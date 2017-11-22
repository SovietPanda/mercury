Building a Development Environment for Mercury
----------------------------------------------

In this guide we will discuss how to setup a Mercury development environment on linux and osx. Microsoft Windows is not
supported in this guide and we suggest that windows users provision a Linux VM for Mercury development.


The Code
~~~~~~~~

Mercury sources are divided into three major repositories.

mercury
_______

This is the main repository for the mercury project. This documentation source (and much more) can be found in the main
repository's *docs* directory. The repo includes the core mercury packages: common, inventory, rpc, and log. It's super
important and you should clone it now.


.. code-block:: bash

    $ git clone https://github.com/jr0d/mercury.git


mercury-api
___________

The mercury_api repository contains the mercury HTTP API and provides a convenient interface to the mercury inventory
and rpc ZeroMQ services. Clone this repository.

.. code-block:: bash

    $ git clone https://github.com/jr0d/mercury-api.git


mercury-agent
_____________

The agent is designed to run on target devices running a Linux operating system. Regardless of your development
operating system, go ahead and clone it now. We'll circle back at the end of this guide.

.. code-block:: bash

    $ git clone https://github.com/jr0d/mercury-agent.git


Install Python 3.6 and virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This process will very per your distribution. It is here for the uninitiated, if you already
have a working python3.6 development environment, you can skip to `Installing service dependencies`_


Enterprise Linux 7 / CentOS 7
_____________________________

.. code-block:: bash

    yum install -y https://mirror.rackspace.com/ius/stable/CentOS/7/x86_64/ius-release-1.0-15.ius.centos7.noarch.rpm && \
    yum install -y python36u python36u-pip && \
    pip3.6 install virtualenv

Ubuntu 16.04
____________

For python 3.6 (preferred)

.. code-block:: bash

    apt-get update && \
    apt-get -y install software-properties-common && \
    add-apt-repository -y ppa:jonathonf/python-3.6 && \
    apt-get update && \
    apt-get -y install python3.6 wget && \
    wget https://bootstrap.pypa.io/get-pip.py -O - | python3.6 && \
    pip3.6 install virtualenv

For python3.5, just install the python3.5-dev and python3.5-pip packages. Then:

.. code-block:: bash

    pip3 install virtualenv


OSX
___

Use homebrew to install python

.. code-block:: bash

    brew install python3
    pip3 install virtualenv


Installing service dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mercury utilizes mongodb for persistent storage and redis for distributed queuing. Install both of these
services using your distributions package management system or use the docker method (see next section)
before proceeding.


Using docker to run mongodb and redis
_____________________________________

On mac, the easiest way to get a development environment up and running is to launch mongo and redis in ephemeral
containers.

.. note::

    Any data that is added to the services running within the container is lost when the container exits. This is
    fine for mercury development, which does not require any table bootstrapping. If you would like to preserve
    your data for more than one session, take a look at the docker
    `volume <https://docs.docker.com/engine/reference/commandline/volume_create/>`_ command

Docker hub provides first party mongo and redis library images. To run both services, use the following commands:

.. code-block:: bash

    $ docker run -p 27017:27017 mongo
    $ docker run -p 6379:6379 redis

This will launch both services in their own containers and forward their service port to your local environment.
To run the commands in the background, use the *-d* flag:

.. code-block:: bash

    $  ~ : docker run -dp 27017:27017 mongo
    b639809a68ff7525869ce799605f0001251169cb4e65407b56712471e8389cb8  <-- The container id
    $  ~ : docker run -dp 6379:6379 redis
    452e3997d6833df75dea1aad2cc966975605fa4d17a080e3e5f38710fa7a5433

You can see that they are running with the *ps* command

.. code-block:: bash

    $  ~ : docker ps
    CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                              NAMES
    452e3997d683        redis                  "docker-entrypoint..."   3 minutes ago       Up 3 minutes        0.0.0.0:6379->6379/tcp             pensive_poincare
    b639809a68ff        mongo                  "docker-entrypoint..."   4 minutes ago       Up 4 minutes        0.0.0.0:27017->27017/tcp           zen_albattani

When you are done with them, stop them with the kill command

.. code-block:: bash

    $  ~ : docker kill 452e3997d683
    452e3997d683
    $  ~ : docker kill b639809a68ff
    b639809a68ff

.. See :ref:`docker` for more information Docker and functionality provided via
	Docker-Compose.

Mercury Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a virtual environment
____________________________

.. code-block:: bash

   $ mkdir ~/.virtualenvs
   $ virtualenv -p`which python3.6` ~/.virtualenvs/mercury


Now activate the virtual environment.


.. code-block:: bash

   $ source ~/.virtualenvs/mercury/bin/activate


.. note::

   You will need to activate the virtual environment whenever you are running a mercury service.
   To make virtualenv management easier, consider using
   `virtualenvwrapper <http://virtualenvwrapper.readthedocs.io/en/latest/install.html>`_ or
   `pyvenv <https://docs.python.org/3/library/venv.html>`_.


Installing the services
_______________________

Mercury implements a micro-services architecture. This allows us to deploy and scale components
independently. Unfortunately, such an architecture slightly complicates the development process
when compared to a monolithic application. Instead of installing and running a single service
element, we must install and run several components.

The first component is the mercury-common package. This package, as the name implies, contains
common libraries used by two or more discrete components. Following common, are the mercury-inventory,
mercury-log, and mercury-rpc packages.

We'll install each package using pip -e. This is synonymous with using *setup.py devel*, but pip allows
us to use library wheelhouses for binary dependencies, such as ZeroMQ or pyYAML, when resolving requirements.


From the mercury repository root:

.. code-block:: bash

    pushd src/mercury-common && \
    pip install -r test-requirements.txt && \
    pip install -e . && \
    popd && \
    pushd src/mercury-inventory && \
    pip install -e . && \
    popd && \
    pushd src/mercury-rpc && \
    pip install -e . && \
    popd && \
    pushd src/mercury-log && \
    pip install -e . && \
    popd


Install the HTTP API in the same manner

.. code-block:: bash

    cd mercury-api && pip install -e .


Creating the Configuration Files
________________________________

All mercury services are configured using a YAML configuration file. Included with each source is a
sample file. The files are already ready for local development for the most part, so we only need
to copy them to a location mercury scans. By default, mercury scans the following directories:

* . (The current working directory)
* ~/.mercury
* /etc/mercury

.. note::

    Once the **find_configuration()** function *finds* the configuration file it is looking for,
    the loop breaks. If you happen to have a configuration file in your local directory and in /etc/mercury,
    the configuration in /etc/mercury will be ignored.

For easy use, we will be populating our configuration files in our home directory, **~/.mercury**. Keep in mind,
Mercury is under heavy development, so watch for changes to the configuration file samples when pulling master; making
sure to update your local copies when necessary.

From the mercury repository root:

.. code-block:: bash

    mkdir -p ~/.mercury && \
    for _package in mercury-inventory mercury-rpc mercury-log; \
    do cp src/${_package}/${_package}-sample.yaml ~/.mercury/${_package}.yaml; done


Running the Services
____________________

When installing mercury packages, the following servers launchers are created:

+--------------------+------------------------------+----------------+------------------------+
| *Program*          | *Description*                | *Default Port* | *Config file*          |
+--------------------+------------------------------+----------------+------------------------+
| mercury-inventory  | Starts the inventory service | 9000           | mercury-inventory.yaml |
+--------------------+------------------------------+----------------+------------------------+
| mercury-frontend   | Starts the frontend service  | 9001           | mercury-rpc.yaml       |
+--------------------+------------------------------+----------------+------------------------+
| mercury-backend    | Starts the backend service   | 9002           | mercury-rpc.yaml       |
+--------------------+------------------------------+----------------+------------------------+
| mercury-rpc-worker | Starts RPC manager process   | N/A            | mercury-rpc.yaml       |
+--------------------+------------------------------+----------------+------------------------+
| mercury-log        | Starts the log service       | 9006           | mercury-log.yaml       |
+--------------------+------------------------------+----------------+------------------------+

Each command line launcher can be configured using the configuration file,
command line arguments, or with environment variables. Running a command with
the --help switch will expose all available options for that service.

For development, starting the services from the command line may not be
desirable. Especially if you are working in an IDE and would like to do things
like attaching a debugger. For these cases, it is possible to launch the python
scripts directly.


* mercury-inventory

  * Inventory Service | *python src/mercury-inventory/mercury/inventory/server.py*

* mercury-rpc

  * Front End ZeroMQ service | **python src/mercury-rpc/mercury/rpc/frontend/frontend.py**
  * Back End ZeroMQ service  | **python src/mercury-rpc/mercury/rpc/backend/backend.py**
  * Workers service          | **python src/mercury-rpc/mercury/rpc/workers/worker.py**

* mercury-log

  * Logging service | **python src/mercury-log/log_service/server.py**

Regardless of how you choose to start the services, make sure they are all
running before proceeding.

Starting the API
________________

The API service has not matured to the point where it has a dedicated service
launcher. To start the service, run the python file directly.

* mercury-api

  * Bottle API service | *python mercury-api/mercury_api/frontend.py*

Running the Agent
~~~~~~~~~~~~~~~~~

Linux (Native)
______________

Following the same pattern as before, copy the agent configuration file to a place mercury will search

.. code-block:: bash

    mkdir -p ~/.mercury
    cp mercury-agent/mercury-agent-sample.yaml ~/.mercury/mercury-agent.yaml


Install the agent into the same virtual environment as the other services, see `Create a virtual environment`_.

.. code-block:: bash

    cd mercury-agent ; pip install -e .

Now you can run the agent with:

.. code-block:: bash

    $ mercury-agent

.. note::

    You should probably run the mercury agent as a normal user for now. TODO: Create a link to the
    press development integration documentation


Running the Agent in Docker on Mac
__________________________________

Running the agent natively on MacOS is not possible due to the agent's dependence on the Linux ABI. Docker for mac,
fortunately, use a linux VM to host containers, making it an excellent target for running the agent.

.. note::
    Docker allows us to quickly develop on the RPC stack of mercury, without having to go through the process of spinning
    up a dedicated VM. If you need to develop on hardware native components, protected ABI inspectors, or press
    provisioning, follow this guide for setting up a development VM and network:

        TODO: Provide link to Agent development guide.

To take advantage of this awesomeness, you need to install `Docker on your mac <https://docs.docker.com/docker-for-mac/install/>`_.

A docker file and configuration file (built specifically for local development on a mac) is provided with the
agent source. The docker file contains the following:

.. code-block:: Dockerfile

    FROM python
    WORKDIR /
    ADD . /src/mercury/agent
    ADD docker/mercury-agent-docker.yaml /etc/mercury/mercury-agent.yaml
    RUN pip install -r /src/mercury/agent/requirements.txt
    RUN pip install -e /src/mercury/agent
    RUN apt-get -y update
    RUN apt-get -y install pciutils
    EXPOSE 9003
    EXPOSE 9004


.. warning::

    The docker build script installs the mercury-common package from pypi, and will not use any local copy. If you
    are making changes to common that you want the agent to take advantage of, copy the provided docker file, and
    modify it to look like this:

    .. code-block:: Dockerfile

        FROM python
        WORKDIR /
        ADD . /src/mercury/agent
        ADD docker/mercury-agent-docker.yaml /etc/mercury/mercury-agent.yaml
        ADD ### PATH TO LOCAL MERCURY COMMON SOURCE ### /src/mercury/common
        RUN pip install -e /src/mercury/common
        RUN pip install -e /src/mercury/agent
        RUN apt-get -y update
        RUN apt-get -y install pciutils
        EXPOSE 9003
        EXPOSE 9004

    Then, run this command to build

    .. code-block:: bash

        $ docker build -f PATH_TO_DOCKERFILE -t mercury/agent .


Build the image with the following

.. code-block:: bash

    $ cd mercury-agent
    $ docker build -t mercury/agent .

Now, run the agent

.. code-block:: bash

    $ docker run -p 9003:9003 -p 9004:9004 mercury/agent mercury-agent

If everything goes correctly you should see output similar to:

.. code-block:: default

    INFO:mercury:Starting Agent
    INFO:mercury.agent.agent:Running inspectors
    INFO:mercury.agent.agent:Registering device inventory for MercuryID 00fc6ad81ffb792d04a7a4454a4c9af4579f9af982
    INFO:mercury.agent.agent:Starting pong service
    INFO:mercury.agent.agent:Registering device
    INFO:mercury.agent.agent:Injecting MercuryID for remote logging
    INFO:mercury.agent.agent:Injection completed
    ERROR:mercury.agent.agent:Caught recoverable exception running async inspector: Could not find lldplite binary
    INFO:mercury.agent.agent:Starting agent rpc service: tcp://0.0.0.0:9003
    INFO:mercury.common.transport:Bound: tcp://0.0.0.0:9003

If you check the backend console you should also see the successful connection:

.. code-block:: default

    2017-10-17 16:46:07,429 : INFO - mercury.rpc.active_asyncio - Adding record, 00fc6ad81ffb792d04a7a4454a4c9af4579f9af982, to active state


Testing out the API
~~~~~~~~~~~~~~~~~~~

Now that everything is up and running, we can begin using the HTTP API to explore the inventory and rpc systems. Try
pointing your browser here: http://localhost:9005/api/active/computers

You should see something like this:

.. code-block:: json

    {
        "total": 1,
        "limit": 250,
        "items": [
            {
                "_id": "59e518dd72bb0a572a05cf08",
                "mercury_id": "00fc6ad81ffb792d04a7a4454a4c9af4579f9af982"
            }
        ],
        "direction": "ASCENDING"
    }

That's your lonely little agent running all by it's lonesome. You can enumerate the agent's RPC capabilities by
hitting the active API with the mercury_id http://localhost:9005/api/active/computers/<mercury_id>

To see it's full inventory record, hit the inventory endpoint http://localhost:9005/api/inventory/computers/<mercury_id>

Now for the fun part, let's try scheduling a job!


.. code-block:: bash

    curl -H 'Content-type: application/json' -d @- -XPOST http://localhost:9005/api/rpc/jobs << EOF
    {
      "query": {},
      "instruction": {
        "method": "echo",
        "args": [
          "Hello Mercury!"
        ]
      }
    }
    EOF

Your consoles should light up and you should get a some JSON back, containing a job_id

.. code-block:: json

    {"job_id": "314ac71b-d353-46e9-95c8-f2e72c3a4f77"}

Try the following urls to inspect the job

* http://localhost:9005/api/rpc/jobs/<job_id>
* http://localhost:9005/api/rpc/jobs/<job_id>/status
* http://localhost:9005/api/rpc/jobs/<job_id>/tasks


Done!
~~~~~

Pat yourself on the back! You are now be ready to begin hacking on Mercury! For full API documentation, be sure to
check out the `API docs <https://jr0d.github.io/mercury_api_docs>`_.

TODO: List mercury resources, slack, irc, mailing list, etc


References
~~~~~~~~~~

`Installing python on OSX <http://www.marinamele.com/2014/07/install-python3-on-mac-os-x-and-use-virtualenv-and-virtualenvwrapper.html>`_
