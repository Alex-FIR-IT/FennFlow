from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from fennflow._decorators import reraise_with
from fennflow._operations.dto import OperationRecord
from fennflow._operations.enums import OperationStatusEnum, OperationTypeEnum
from fennflow._query_specs.insert.insert import InsertQuerySpec
from fennflow._query_specs.select.is_empty import IsEmptyQuerySpec
from fennflow.backends.enums import OnConflictDoEnum
from fennflow.reconciler.enums import ReconcileStrategyEnum
from fennflow.reconciler.exceptions import ReconcileFailedException
from fennflow.repositories import RepoField

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Generator, Iterable
    from uuid import UUID

    from fennflow import UnitOfWork
    from fennflow._new_types import BackendScope
    from fennflow.backends._core import BackendOrchestrator
    from fennflow.connectors._abstract import AbstractConnector
    from fennflow.repositories.fields.base import RepoExtra
    from fennflow.responses.list import ListResponse

logger = logging.getLogger(__name__)


reconcile_to_on_conflict_strategy = {
    ReconcileStrategyEnum.REPLACE: OnConflictDoEnum.REPLACE,
    ReconcileStrategyEnum.INSERT_MISSING: OnConflictDoEnum.DO_NOTHING,
    ReconcileStrategyEnum.FILL_IF_EMPTY: OnConflictDoEnum.RAISE,
}


class Reconciler:
    """Synchronizes backend state with actual connector (storage) state.

    On startup or session start, the backend may be out of sync with the
    real storage (e.g. on first connection with a persistent backend).
     ``Reconciler`` restores consistency
    by listing files from the connector and inserting them into the backend
    according to the chosen strategy.
    Called internally by ``ReconcileOrchestrator`` in UnitOfWork.__aenter__.

    Notes:
        Reconciler does not perform garbage collection!

    Example::

        import asyncio

        from fennflow.reconciler import Reconciler, ReconcileStrategyEnum
        from fennflow.uow import UowInspector


        async def main():
            async with UOW() as uow:
                uow_inspector = UowInspector(uow=uow)
                reconcile = Reconciler(
                    uow_fields=uow_inspector.get_repo_fields(),
                    connector=uow.connector,
                    backend=uow.backend,
                    )
                await reconcile.reconcile(
                    session_id=uow._session_id,
                    batch_size=500,
                    strategy=ReconcileStrategyEnum.REPLACE,
                    backend_scope=uow.config["connector"].scope
                    )

        if __name__ == "__main__":
            asyncio.run(main())
    """

    def __init__(
        self,
        uow_fields: Iterable[RepoField],
        backend: BackendOrchestrator,
        connector: AbstractConnector,
    ) -> None:
        """Init method.

        Args:
            uow_fields: Repository field descriptors to reconcile.
                Each field provides the namespace and repo config needed to
                list objects from the connector.
            backend: The backend to sync state into.
            connector: The storage connector to read the source-of-truth from.
        """
        self.uow_fields = uow_fields
        self.backend = backend
        self.connector = connector

    @reraise_with(ReconcileFailedException())
    async def reconcile(
        self,
        session_id: UUID,
        strategy: ReconcileStrategyEnum,
        batch_size: int,
        backend_scope: BackendScope,
    ) -> None:
        """Reconcile all registered repository fields against the connector.

        Iterates over each ``RepoField``, lists its objects from the connector
        in pages, and inserts them into the backend. The conflict resolution
        behavior is determined by ``strategy``.

        Args:
            session_id: Session ID to stamp on inserted ``OperationRecord``s.
            strategy: Controls whether to skip reconciliation, overwrite existing
                records, or only insert missing ones. See ``ReconcileStrategyEnum``.
            batch_size: Number of objects to fetch per page from the connector.
            backend_scope: Scope to assign to inserted records in the backend.

        Raises:
            ReconcileFailedException: If any error occurs during reconciliation.
        """
        if not await self._should_reconcile(
            strategy=strategy,
            backend_scope=backend_scope,
        ):
            return

        for repo in self.uow_fields:
            on_conflict = reconcile_to_on_conflict_strategy[strategy]

            async for page in self._iter_pages(repo, batch_size=batch_size):
                await self.backend.backend_engine.execute(
                    InsertQuerySpec.from_operations(
                        operations=self._records_from_page(
                            session_id=session_id,
                            page=page,
                            repo_extra=repo.repo_extra,
                            backend_scope=backend_scope,
                        ),
                        on_conflict=on_conflict,
                    )
                )

    async def _should_reconcile(
        self,
        strategy: ReconcileStrategyEnum,
        backend_scope: BackendScope,
    ) -> bool:
        if strategy == ReconcileStrategyEnum.FILL_IF_EMPTY:
            return await self.backend.backend_engine.execute(
                IsEmptyQuerySpec(scope=backend_scope)
            )
        return True

    async def _iter_pages(
        self,
        repo: RepoField,
        batch_size: int,
    ) -> AsyncGenerator[ListResponse, None]:
        continuation_token = None

        while True:
            page = await self.connector.list_objects(
                prefix="",
                limit=batch_size,
                repo_extra=repo.repo_extra,
                continuation_token=continuation_token,
            )

            if not page.storage_paths:
                break

            yield page

            if page.continuation_token is None:
                break
            continuation_token = page.continuation_token

    @staticmethod
    def _records_from_page(
        session_id: UUID,
        page: ListResponse,
        repo_extra: RepoExtra,
        backend_scope: str,
    ) -> Generator[OperationRecord, None, None]:
        for storage_path in page:
            yield OperationRecord.create(
                session_id=session_id,
                storage_path=storage_path,
                operation_type=OperationTypeEnum.PUT,
                status=OperationStatusEnum.UPLOADED,
                repo_extra=repo_extra,
                scope=backend_scope,
            )

    @staticmethod
    def _get_repo_fields(uow: UnitOfWork) -> Generator[RepoField, None, None]:
        for field in vars(type(uow)).values():
            if isinstance(field, RepoField):
                yield field
