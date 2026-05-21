from collections import defaultdict

from fennflow._new_types import BackendScope, Namespace, StoragePath
from fennflow._operations.dto import Record
from fennflow._query_specs.base import BaseQuerySpec
from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow

ScopedStorageType = dict[tuple[Namespace, StoragePath], Record]
InMemoryStorageType = defaultdict[BackendScope, ScopedStorageType]
QueryFlowRegistryType = dict[type[BaseQuerySpec], BaseInMemoryBackendQueryFlow]
