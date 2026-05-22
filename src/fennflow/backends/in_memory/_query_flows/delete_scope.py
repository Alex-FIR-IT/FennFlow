from dataclasses import dataclass

from fennflow._query_specs.delete.delete_scope import DeleteScopeQuerySpec
from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow


@dataclass(slots=True)
class DeleteScopeFlow(BaseInMemoryBackendQueryFlow[DeleteScopeQuerySpec, None]):
    async def run(
        self,
        query_spec: DeleteScopeQuerySpec,
    ) -> None:
        self.storage.pop(query_spec.scope, None)
