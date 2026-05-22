from __future__ import annotations

from dataclasses import dataclass

from fennflow._query_specs.update.merge import MergeQuerySpec
from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow


@dataclass(slots=True)
class MergeFlow(BaseInMemoryBackendQueryFlow[MergeQuerySpec, None]):
    async def run(
        self,
        query_spec: MergeQuerySpec,
    ) -> None:
        for record in query_spec.records:
            self.storage[record.scope][(record.namespace, record.storage_path)] = record
