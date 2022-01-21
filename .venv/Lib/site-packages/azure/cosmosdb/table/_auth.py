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

from azure.cosmosdb.table.common._auth import (
    _StorageSharedKeyAuthentication,
)

import logging
logger = logging.getLogger(__name__)


class _StorageTableSharedKeyAuthentication(_StorageSharedKeyAuthentication):
    def sign_request(self, request):
        string_to_sign = \
            self._get_verb(request) + \
            self._get_headers(
                request,
                ['content-md5', 'content-type', 'x-ms-date'],
            ) + \
            self._get_canonicalized_resource(request) + \
            self._get_canonicalized_resource_query(request)

        self._add_authorization_header(request, string_to_sign)
        logger.debug("String_to_sign=%s", string_to_sign)

    def _get_canonicalized_resource_query(self, request):
        for name, value in request.query.items():
            if name == 'comp':
                return '?comp=' + value
        return ''
