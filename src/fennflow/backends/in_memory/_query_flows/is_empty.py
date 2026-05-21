from __future__ import annotations

from dataclasses import dataclass

from fennflow._query_specs.select.is_empty import IsEmptyQuerySpec
from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow


@dataclass(slots=True)
class IsEmptyFlow(BaseInMemoryBackendQueryFlow[IsEmptyQuerySpec, bool]):
    async def run(
        self,
        query_spec: IsEmptyQuerySpec,  # noqa: ARG002
    ) -> bool:
        scoped_storage = self.storage.get(query_spec.scope, {})
        return len(scoped_storage) == 0
