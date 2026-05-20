from __future__ import annotations

from dataclasses import dataclass

from fennflow._query_specs.select.select_visible import SelectVisibleQuerySpec
from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow
from fennflow.backends.in_memory._select import SelectOperation
from fennflow.backends.responses import RecordPage


@dataclass(slots=True)
class SelectVisibleFlow(
    BaseInMemoryBackendQueryFlow[SelectVisibleQuerySpec, RecordPage]
):
    async def run(
        self,
        query_spec: SelectVisibleQuerySpec,
    ) -> RecordPage:
        return SelectOperation(
            prefix=query_spec.prefix,
            continuation_token=query_spec.continuation_token,
            limit=query_spec.limit,
            visible_for_session_id=query_spec.session_id,
        ).select(record=self.scoped_storage.values())
