from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow

if TYPE_CHECKING:
    from fennflow._query_specs.update.merge import MergeQuerySpec


@dataclass(slots=True)
class MergeFlow(BaseInMemoryBackendQueryFlow):
    async def run(
        self,
        query_spec: MergeQuerySpec,
    ) -> None:
        for operation in query_spec.operations:
            self.scoped_storage[operation.storage_path] = operation
