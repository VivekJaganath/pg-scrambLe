"""
Copyright (c) 2015 SONATA-NFV
ALL RIGHTS RESERVED.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission.
This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the SONATA
partner consortium (www.sonata-nfv.eu).a
"""
"""
This is SONATA's service lifecycle management plugin
"""

import os
from urllib.parse import urlparse

# List of topics that are used by the SLM for its rabbitMQ communication

# With gatekeeper
GK_CREATE = "service.instances.create"
GK_PAUSE = "service.instance.pause"
GK_RESUME = "service.instance.restart"
GK_KILL = "service.instance.terminate"
GK_UPDATE = "service.instances.update"

# With other SLM
MANO_STATE = "mano.share.state"
MANO_CREATE = "mano.instances.create"
MANO_PAUSE = "mano.instance.pause"
MANO_RESUME = "mano.instance.restart"
MANO_KILL = "mano.instance.terminate"
MANO_UPDATE = "mano.instances.update"
MANO_DEPLOY = "mano.function.deploy"
MANO_CS_DEPLOY = "mano.cloud_service.deploy"
MANO_PLACE = "mano.service.place"
MANO_START = "mano.function.start"
MANO_CONFIG = "mano.function.configure"
MANO_STOP = "mano.function.stop"
MANO_SCALE = "mano.function.scale"
MANO_SCALING = "mano.service.scaling"

# With gatekeeper or other SLM
WC_CREATE = "*.instances.create"
WC_PAUSE = "*.instance.pause"
WC_RESUME = "*.instance.restart"
WC_KILL = "*.instance.terminate"
WC_UPDATE = "*.instances.update"

# With infrastructure adaptor
IA_DEPLOY = 'infrastructure.function.deploy'
IA_REMOVE = 'infrastructure.service.remove'
IA_TOPO = 'infrastructure.management.compute.list'
IA_PREPARE = 'infrastructure.service.prepare'
IA_CONF_CHAIN = 'infrastructure.service.chain.configure'
IA_DECONF_CHAIN = 'infrastructure.service.chain.deconfigure'
IA_CONF_WAN = 'infrastructure.service.wan.configure'
IA_DECONF_WAN = 'infrastructure.service.wan.deconfigure'

# With specific manager registry
SRM_ONBOARD = 'specific.manager.registry.ssm.on-board'
SRM_INSTANT = 'specific.manager.registry.ssm.instantiate'
SRM_UPDATE = 'specific.manager.registry.ssm.update'
SSM_TERM = 'specific.manager.registry.ssm.terminate'
FSM_TERM = 'specific.manager.registry.fsm.terminate'

# With Executive
EXEC_PLACE = 'placement.executive.request'

# With plugin mananger
PL_STATUS = "platform.management.plugin.status"

# With monitoring
MON_RECEIVE = "son.monitoring"
FROM_MON_SSM = "monitor.ssm."

# REST APIs
temp = os.environ.get("url_gk_api")
if temp is None:
    temp = "http://son-gtkapi:5000/api/v2/"
p = urlparse(temp)
GK_PORT = p.port
BASE_URL = p.scheme + "://" + p.hostname + ":" + str(GK_PORT)
API_VER = '/api/v2'
PUPLIC_KEY_PATH = '/public-key'
REG_PATH = '/micro-services'
LOGIN_PATH = '/micro-services'
SERVICES = '/services/'
COMPLEX_SERVICES = '/complex-services/'
FUNCTIONS = '/functions/'
CLOUD_SERVICES = '/cloud-services/'

GK_REGISTER = BASE_URL + API_VER + REG_PATH
GK_LOGIN = BASE_URL + API_VER + LOGIN_PATH
GK_SERVICES = BASE_URL + API_VER + SERVICES
GK_COMPLEX_SERVICES = BASE_URL + API_VER + COMPLEX_SERVICES
GK_FUNCTIONS = BASE_URL + API_VER + FUNCTIONS
GK_CLOUD_SERVICES = BASE_URL + API_VER + CLOUD_SERVICES

# REST API with GK
GK_SERVICES_URL = BASE_URL + '/api/v2/services/'
GK_FUNCTIONS_URL = BASE_URL + '/api/v2/functions/'

# With Repositories
temp = os.environ.get("url_nsr_repository")
if temp is None:
    temp = "http://son-catalogue-repos:4011/api/v2/"
c = urlparse(temp)
CAT_PORT = c.port
CAT_BASE_URL = c.scheme + "://" + c.hostname + ":" + str(CAT_PORT)

NSR_REPOSITORY_URL = CAT_BASE_URL + "/records/nsr/"
COSR_REPOSITORY_URL = CAT_BASE_URL + "/records/cosr/"
VNFR_REPOSITORY_URL = CAT_BASE_URL + "/records/vnfr/"
CSR_REPOSITORY_URL = CAT_BASE_URL + "/records/csr/"

# With Monitoring Manager
# TODO: Secure this get against failure
MONITORING_URL = os.environ.get("url_monitoring_server")
