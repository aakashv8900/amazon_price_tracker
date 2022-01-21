# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from azure.cosmosdb.table.common._constants import (
    __author__,
    __version__,
    DEFAULT_X_MS_VERSION,
)
from azure.cosmosdb.table.common.cloudstorageaccount import CloudStorageAccount
from azure.cosmosdb.table.common.models import (
    RetentionPolicy,
    Logging,
    Metrics,
    CorsRule,
    DeleteRetentionPolicy,
    StaticWebsite,
    ServiceProperties,
    AccessPolicy,
    ResourceTypes,
    Services,
    AccountPermissions,
    Protocol,
    ServiceStats,
    GeoReplication,
    LocationMode,
    RetryContext,
)
from azure.cosmosdb.table.common.retry import (
    ExponentialRetry,
    LinearRetry,
    no_retry,
)
from azure.cosmosdb.table.common.sharedaccesssignature import (
    SharedAccessSignature,
)
from azure.cosmosdb.table.common.tokencredential import TokenCredential
from azure.cosmosdb.table.common._error import AzureSigningError
