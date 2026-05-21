from dataclasses import dataclass

from fennflow._operations.dto import Record
from fennflow._query_specs.select.get_by_storage_path import GetByStoragePathQuerySpec
from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow


@dataclass(slots=True)
class GetByStoragePathFlow(
    BaseInMemoryBackendQueryFlow[GetByStoragePathQuerySpec, Record | None]
):
    async def run(
        self,
        query_spec: GetByStoragePathQuerySpec,
    ) -> Record | None:
        scoped_storage = self.storage.get(query_spec.scope, {})
        return scoped_storage.get((query_spec.namespace, query_spec.storage_path))
