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
import os
from setuptools import setup


def find_mercury_packages():
    """Fix for easily finding mercury packages and subpackages"""
    packages = []
    for container, _, items in os.walk('mercury'):
        if '__init__.py' in items:
            packages.append(container.replace('/', '.'))
    return packages


def get_version():
    with open('../../VERSION') as fp:
        return fp.readline().strip()


setup(
    name='mercury-inventory',
    version=get_version(),
    packages=find_mercury_packages(),
    url='http://www.mercurysoft.io',
    license='Apache-2.0',
    author='Jared Rodriguez',
    author_email='jared.rodriguez@rackspace.com',
    description='Mercury inventory controller',
    install_requires=[
        'msgpack-python',
        'pyzmq',
    ],
)
