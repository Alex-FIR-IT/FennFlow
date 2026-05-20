from __future__ import annotations

from typing import Any

from fennflow._operations.context.delete import DeleteContext
from fennflow._operations.dto import OperationRecord, Record
from fennflow._operations.enums import OperationTypeEnum

from .._query_specs.select.get_visible import GetVisibleQuerySpec
from ..backends.enums import OnConflictDoEnum
from .at import AtRepository


class DeleteRepository(AtRepository):
    """Repository mixin for deleting files from storage.

    Implements Saga-based deletion with automatic compensation on failure.
    """

    async def delete(self, path: str, **provider_extra: Any) -> bool:
        """Delete a file from storage.

        Args:
            path: Path to the file relative to the current directory.
            **provider_extra: Additional kwargs forwarded to the connector.

        Returns:
            True if the file was deleted, False if it did not exist.

        """
        storage_path = self._join_path(path)
        record = await self._uow._backend.backend_engine.execute(
            GetVisibleQuerySpec(
                storage_path=storage_path,
                current_session_id=self._uow._session_id,
            )
        )
        if record is None:
            return False

        operation = OperationRecord.from_uow(
            uow=self._uow,
            operation_type=OperationTypeEnum.DELETE,
            storage_path=record.storage_path,
            context=self.__get_context(record=record),
            repo_extra=self.repo_extra,
        )
        await self._uow.backend.insert(
            operation,
            on_conflict=OnConflictDoEnum.REPLACE,
        )

        await self._uow._operation_executor.execute(
            operation,
            **provider_extra,
        )
        await self._uow.backend.flush(operations=[operation])
        return True

    def __get_context(self, record: Record) -> DeleteContext:
        return DeleteContext(
            to_storage_path=record.generate_tmp_path(),
            to_namespace=self.repo_extra["namespace"],
        )
