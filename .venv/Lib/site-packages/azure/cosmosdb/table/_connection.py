# -------------------------------------------------------------------------
# Copyright (c) Microsoft.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------

from azure.cosmosdb.table.common._constants import (
    SERVICE_HOST_BASE,
    DEFAULT_PROTOCOL,
)

from azure.cosmosdb.table.common._connection import (
    _ServiceParameters,
    _EMULATOR_ENDPOINTS,
    _CONNECTION_ENDPOINTS,
    _CONNECTION_ENDPOINTS_SECONDARY,
)

from ._constants import (
    DEV_TABLE_HOST,
)

_EMULATOR_ENDPOINTS['table'] = DEV_TABLE_HOST
_CONNECTION_ENDPOINTS['table'] = 'TableEndpoint'
_CONNECTION_ENDPOINTS_SECONDARY['table'] = 'TableSecondaryEndpoint'

class _TableServiceParameters(_ServiceParameters):
    def __init__(self, service, account_name=None, account_key=None, sas_token=None,
                 is_emulated=False, protocol=DEFAULT_PROTOCOL, endpoint_suffix=SERVICE_HOST_BASE,
                 custom_domain=None, custom_domain_secondary=None):

        super(_TableServiceParameters, self).__init__(service, account_name, account_key, sas_token,
                 is_emulated, protocol, endpoint_suffix, custom_domain, custom_domain_secondary)
