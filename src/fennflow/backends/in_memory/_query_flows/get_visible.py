from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow

if TYPE_CHECKING:
    from fennflow._operations.dto import OperationRecord
    from fennflow._query_specs.select.get_visible import GetVisibleQuerySpec


@dataclass(slots=True)
class GetVisibleFlow(BaseInMemoryBackendQueryFlow):
    async def run(
        self,
        query_spec: GetVisibleQuerySpec,
    ) -> OperationRecord | None:
        db_record = self.scoped_storage.get(query_spec.storage_path)

        if db_record is not None and (
            db_record.is_uploaded
            or (
                db_record.is_pending
                and db_record.session_id == query_spec.current_session_id
                and db_record.is_upserting_type
            )
        ):
            return db_record

        return None
