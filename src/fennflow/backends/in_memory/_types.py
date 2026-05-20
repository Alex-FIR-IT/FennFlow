from collections import defaultdict

from fennflow._new_types import BackendScope, StoragePath
from fennflow._operations.dto import OperationRecord, Record
from fennflow._query_specs.base import BaseQuerySpec
from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow

ScopedStorageType = dict[StoragePath, Record]
InMemoryStorageType = defaultdict[BackendScope, ScopedStorageType]
QueryFlowRegistryType = dict[type[BaseQuerySpec], BaseInMemoryBackendQueryFlow]
