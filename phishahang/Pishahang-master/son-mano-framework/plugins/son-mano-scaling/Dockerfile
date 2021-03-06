# Copyright (c) 2015 SONATA-NFV
# ALL RIGHTS RESERVED.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
# This work has been performed in the framework of the SONATA project,
# funded by the European Commission under Grant number 671517 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.sonata-nfv.eu).

FROM python:3.5
MAINTAINER SONATA

# define plugin name once
ENV PLUGIN_BASE son-mano-scaling
# Configuration
ENV broker_host amqp://guest:guest@son-broker:5672/%2F
ENV broker_exchange son-kernel

# FIXME: Someother way to change this
ENV PARENT_IP vm-hadik3r-08.cs.uni-paderborn.de
ENV DUMMY_INSTANCE_IP sonatamano.cs.upb.de

# add generic project files
ADD son-mano-base /son-mano-base

# add plugin related files
ADD plugins/${PLUGIN_BASE} /plugins/${PLUGIN_BASE}

# install son-mano-base to be able to use the plugin base class etc.
WORKDIR /son-mano-base
RUN python setup.py install

# install actual plugin
WORKDIR /plugins/${PLUGIN_BASE}
RUN python setup.py develop

# Install python requirements
COPY /plugins/${PLUGIN_BASE}/requirements.txt ./
RUN pip install --no-cache-dir -r /plugins/${PLUGIN_BASE}/requirements.txt

CMD ["son-mano-scaling"]


