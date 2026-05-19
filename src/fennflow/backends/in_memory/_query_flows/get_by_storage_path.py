from dataclasses import dataclass

from fennflow._operations.dto import OperationRecord
from fennflow._query_specs.select.get_by_storage_path import GetByStoragePathQuerySpec
from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow


@dataclass(slots=True)
class GetByStoragePathFlow(BaseInMemoryBackendQueryFlow):
    async def run(
        self,
        query_spec: GetByStoragePathQuerySpec,
    ) -> OperationRecord | None:
        return self.scoped_storage.get(query_spec.storage_path)
