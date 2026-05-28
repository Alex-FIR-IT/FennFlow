from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from fennflow._query_specs.delete.delete_scope import DeleteScopeQuerySpec
from fennflow.connectors import InMemoryConnector
from fennflow.reconciler._orchestrator import ReconcileOrchestrator

if TYPE_CHECKING:
    from fennflow._new_types import BackendScope
    from tests.conftest import TestUOW


async def reset_state(
    uow_cls: type[TestUOW],
    scope: BackendScope,
) -> None:
    async with uow_cls() as uow:
        _, response = await asyncio.gather(
            *[
                uow._backend.backend_engine.execute(DeleteScopeQuerySpec(scope=scope)),
                uow.connector.list_objects(
                    prefix="",
                    repo_extra=uow.user_files.repo_extra,
                ),
            ]
        )

        await asyncio.gather(
            *[
                uow.connector.delete(
                    storage_path=storage_path,
                    repo_extra=uow.user_files.repo_extra,
                )
                for storage_path in response
            ]
        )

    ReconcileOrchestrator._reconciled_on_startup = set()
