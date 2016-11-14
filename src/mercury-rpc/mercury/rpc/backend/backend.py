# Copyright 2015 Jared Rodriguez (jared.rodriguez@rackspace.com)
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import datetime
import logging
import time

from mercury.common.transport import SimpleRouterReqService
from mercury.common.mongo import get_collection, get_connection
from mercury.rpc.configuration import rpc_configuration, get_jobs_collection, get_tasks_collection
from mercury.rpc.db import ActiveInventoryDBController
from mercury.rpc.jobs import (
    is_completed,
    update_task_existing_connection
)
from mercury.rpc.ping import spawn

log = logging.getLogger(__name__)

RPC_CONFIG_FILE = 'mercury-rpc.yaml'


# TODO: Rewrite BackEndService as a general purpose message router


class BackEndService(SimpleRouterReqService):
    def __init__(self, active_db_collection, jobs_collection, tasks_collection):
        registration_service_bind_address = rpc_configuration.get('backend',
                                                                  {}).get('service_url',
                                                                          'tcp://0.0.0.0:9002')
        super(BackEndService, self).__init__(registration_service_bind_address)

        self.active_db_controller = ActiveInventoryDBController(active_db_collection)

        self.jobs_collection = jobs_collection
        self.tasks_collection = tasks_collection

    def process(self, message):
        if message.get('action') == 'register':
            return self.register(data=message.get('client_info'))
        elif message.get('action') == 'task_return':
            return self.task_return(message.get('response'))
        return dict(error=True, message='Did not receive appropriate action')

    def spawn_pinger(self, mercury_id, address, port):
        endpoint = 'tcp://%s:%s' % (address, port)
        spawn(endpoint, mercury_id, self.active_db_controller)

    def reacquire(self):
        existing_documents = self.active_db_controller.query({}, projection={'mercury_id': 1,
                                                                             'rpc_address': 1,
                                                                             'ping_port': 1})
        for doc in existing_documents:
            log.info('Attempting to reacquire %s : %s' % (doc['mercury_id'], doc['rpc_address']))
            self.spawn_pinger(doc['mercury_id'], doc['rpc_address'], doc['ping_port'])

    def register(self, data):
        if not self.active_db_controller.validate(data):
            log.error('Recieved invalid data')
            return dict(error=True, message='Invalid request')

        self.active_db_controller.insert(data)

        self.spawn_pinger(data['mercury_id'], data['rpc_address'], data['ping_port'])

        return dict(error=False, message='Registration successful')

    def task_return(self, response_data):
        """Update Job task with response data and result status
        :param response_data: {
            job_id:
            task_id:
            mercury_id:
            method:
            time_started:
            time_completed:
            data: {
            }
            result: SUCCESS|ERROR|EXCEPTION|TIMEOUT
        }
        :return:
        """
        now = time.time()
        ttl_time = datetime.datetime.utcfromtimestamp(now)

        job_id = response_data['job_id']
        task_id = response_data['task_id']
        update = {
            'status': response_data['result'],  # Naming conventions changed when coding provider
            'time_started': response_data['time_started'],
            'time_completed': response_data['time_completed'],
            'ttl_time_completed': ttl_time,
            'result': response_data['traceback_info'] or response_data['data']
        }

        log.info('Task completed: task_id: {task_id} job: {job_id} result: {result}'.format(
            **response_data
        ))

        update_task_existing_connection(self.tasks_collection, task_id, update)

        if is_completed(self.tasks_collection, job_id):

            log.info('Job completed: {job_id}'.format(job_id=job_id))
            self.jobs_collection.update_one(
                {
                    'job_id': job_id
                },
                {
                    '$set': {
                        'time_completed': now,
                        'ttl_time_completed': ttl_time
                    }
                }
            )

        return dict(message='Accepted')


def rpc_backend_service():
    """
    Entry point

    :return:
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s : %(levelname)s - %(name)s - %(message)s')
    logging.getLogger('mercury.rpc.ping').setLevel(logging.DEBUG)
    logging.getLogger('mercury.rpc.ping2').setLevel(logging.DEBUG)
    db_configuration = rpc_configuration.get('db', {})

    connection = get_connection(server_or_servers=db_configuration.get('rpc_mongo_servers',
                                                                       'localhost'),
                                replica_set=db_configuration.get('replica_set'))

    active_db_collection = get_collection(db_configuration.get('rpc_mongo_db',
                                                               'test'),
                                          db_configuration.get('rpc_mongo_collection',
                                                               'rpc'),
                                          connection)

    jobs_collection = get_jobs_collection(connection)
    tasks_collection = get_tasks_collection(connection)

    jobs_collection.create_index('ttl_time_completed', expireAfterSeconds=3600)
    tasks_collection.create_index('ttl_time_completed', expireAfterSeconds=3600)

    server = BackEndService(active_db_collection, jobs_collection, tasks_collection)
    server.reacquire()
    server.bind()
    server.start()


if __name__ == '__main__':
    rpc_backend_service()
