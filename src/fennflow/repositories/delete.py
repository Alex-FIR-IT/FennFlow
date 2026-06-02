from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fennflow._operations.context.delete import DeleteContext
from fennflow._operations.dto import OperationRecord, Record
from fennflow._operations.enums import OperationTypeEnum
from fennflow._sentinel import OMIT
from fennflow.backends.enums import OnConflictDoEnum
from fennflow.repositories._helper_mixins import gather_tasks, visible_record
from fennflow.repositories.at import AtRepository
from fennflow.responses.connector_raw import ConnectorRawResponse

if TYPE_CHECKING:
    from collections.abc import Coroutine

    from fennflow._new_types import ConnectorExtra


DeleteResponse = list[ConnectorRawResponse[Any] | None]


class DeleteRepository(AtRepository):
    """Repository mixin for deleting files from storage.

    Implements Saga-based deletion with automatic compensation on failure.
    """

    async def delete(
        self,
        *paths: str,
        connector_extra: ConnectorExtra = OMIT,
    ) -> DeleteResponse:
        """Delete files from storage.

        Args:
            paths: Paths to the files relative to the current directory.
            connector_extra: Additional kwargs forwarded to the connector.

        Returns:
            DeleteResponse containing a result per path in the same order as input.
            Each element is a ConnectorRawResponse if the file was deleted,
            or None if the path did not exist in the backend.

        """
        tasks = []
        task_indexes = []
        operations = []
        results: DeleteResponse = [None] * len(paths)

        for task_index, path in enumerate(paths):
            storage_path = self._join_path(path)
            record = await visible_record.get_visible_record(
                repostory=self,
                storage_path=storage_path,
            )

            if record is None:
                continue

            operation = self.__create_operation(record=record)
            await self.__insert_into_buffer(operation=operation)

            tasks.append(self.__construct_executor_task(operation, connector_extra))
            task_indexes.append(task_index)
            operations.append(operation)

        await self._uow.backend.flush(operations=operations)
        return await gather_tasks.gather_tasks(
            tasks=tasks,
            task_indexes=task_indexes,
            results=results,
        )

    def __get_context(self, record: Record) -> DeleteContext:
        return DeleteContext(
            to_storage_path=record.generate_tmp_path(),
            to_namespace=self.repo_extra["namespace"],
        )

    def __create_operation(self, record: Record) -> OperationRecord:
        return OperationRecord.from_uow(
            uow=self._uow,
            operation_type=OperationTypeEnum.DELETE,
            storage_path=record.storage_path,
            context=self.__get_context(record=record),
            repo_extra=self.repo_extra,
        )

    def __construct_executor_task(
        self,
        operation: OperationRecord,
        connector_extra: ConnectorExtra = OMIT,
    ) -> Coroutine[Any, Any, Any]:
        return self._uow._operation_executor.execute(
            operation,
            connector_extra=connector_extra,
        )

    async def __insert_into_buffer(self, operation: OperationRecord) -> None:
        await self._uow.backend.insert(
            operation,
            on_conflict=OnConflictDoEnum.REPLACE,
        )
