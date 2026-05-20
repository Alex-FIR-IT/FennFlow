from __future__ import annotations

from dataclasses import dataclass

from fennflow._operations.dto import Record
from fennflow._query_specs.select.get_visible import GetVisibleQuerySpec
from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow


@dataclass(slots=True)
class GetVisibleFlow(BaseInMemoryBackendQueryFlow[GetVisibleQuerySpec, Record | None]):
    async def run(
        self,
        query_spec: GetVisibleQuerySpec,
    ) -> Record | None:
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
