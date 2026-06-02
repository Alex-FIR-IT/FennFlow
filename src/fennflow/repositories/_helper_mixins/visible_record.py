from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._query_specs.select.get_visible import GetVisibleQuerySpec

if TYPE_CHECKING:
    from fennflow._new_types import StoragePath
    from fennflow._operations.dto import Record
    from fennflow._protocols.repository import RepositoryProtocol


class VisibleRecordHelper:
    async def _get_visible_record(
        self: RepositoryProtocol,
        storage_path: StoragePath,
    ) -> Record | None:
        return await self._uow._backend.backend_engine.execute(
            GetVisibleQuerySpec(
                scope=self._uow._resolved_config.backend.scope,
                namespace=self.repo_extra["namespace"],
                storage_path=storage_path,
                session_id=self._uow._session_id,
            )
        )
