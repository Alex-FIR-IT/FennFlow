from __future__ import annotations

from dataclasses import dataclass

from fennflow._query_specs.select.count import CountQuerySpec
from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow


@dataclass(slots=True)
class CountFlow(BaseInMemoryBackendQueryFlow[CountQuerySpec, int]):
    async def run(
        self,
        query_spec: CountQuerySpec,  # noqa: ARG002
    ) -> int:
        return sum(len(scoped_storage) for scoped_storage in self.storage)
