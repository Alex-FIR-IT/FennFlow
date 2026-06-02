from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._query_specs.select.get_visible import GetVisibleQuerySpec

if TYPE_CHECKING:
    from fennflow._new_types import StoragePath
    from fennflow._operations.dto import Record
    from fennflow._protocols.repository import RepositoryProtocol


async def get_visible_record(
    repostory: RepositoryProtocol,
    storage_path: StoragePath,
) -> Record | None:
    return await repostory._uow._backend.backend_engine.execute(
        GetVisibleQuerySpec(
            scope=repostory._uow._resolved_config.backend.scope,
            namespace=repostory.repo_extra["namespace"],
            storage_path=storage_path,
            session_id=repostory._uow._session_id,
        )
    )
