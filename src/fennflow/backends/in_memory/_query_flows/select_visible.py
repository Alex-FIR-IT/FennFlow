from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow
from fennflow.backends.in_memory._select import SelectOperation

if TYPE_CHECKING:
    from fennflow._query_specs.select.select_visible import SelectVisibleQuerySpec
    from fennflow.backends.responses import OperationPage


@dataclass(slots=True)
class SelectVisibleFlow(BaseInMemoryBackendQueryFlow):
    async def run(
        self,
        query_spec: SelectVisibleQuerySpec,
    ) -> OperationPage:
        return SelectOperation(
            prefix=query_spec.prefix,
            continuation_token=query_spec.continuation_token,
            limit=query_spec.limit,
            visible_for_session_id=query_spec.session_id,
        ).select(record=self.scoped_storage.values())
