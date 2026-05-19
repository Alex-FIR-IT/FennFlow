from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow

if TYPE_CHECKING:
    from fennflow._query_specs.select.is_empty import IsEmptyQuerySpec


@dataclass(slots=True)
class IsEmptyFlow(BaseInMemoryBackendQueryFlow):
    async def run(
        self,
        query_spec: IsEmptyQuerySpec,  # noqa: ARG002
    ) -> bool:
        return len(self.scoped_storage) == 0
