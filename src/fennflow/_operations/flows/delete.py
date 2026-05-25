from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from fennflow._operations.enums import OperationStatusEnum
from fennflow._operations.flows.abstract import AbstractFlow
from fennflow.connectors.exceptions import NoSuchKeyException

if TYPE_CHECKING:
    from fennflow._operations.context.delete import DeleteContext
    from fennflow._operations.dto import OperationRecord
    from fennflow.connectors._abstract import AbstractConnector


class DeleteFlow(AbstractFlow):
    @staticmethod
    async def execute(
        *,
        operation: OperationRecord,
        connector: AbstractConnector,
        **connector_extra,
    ):
        ctx: DeleteContext = operation.context

        with suppress(NoSuchKeyException):
            await connector.copy_object(
                from_storage_path=operation.record.storage_path,
                to_storage_path=ctx.to_storage_path,
                to_namespace=ctx.to_namespace,
                repo_extra=operation.repo_extra,
                **connector_extra,
            )
            return await connector.delete(
                storage_path=operation.record.storage_path,
                repo_extra=operation.repo_extra,
                **connector_extra,
            )

    @staticmethod
    async def compensate(
        *,
        operation: OperationRecord,
        connector: AbstractConnector,
        **connector_extra,
    ):
        ctx: DeleteContext = operation.context
        await connector.copy_object(
            from_storage_path=ctx.to_storage_path,
            to_storage_path=operation.record.storage_path,
            to_namespace=operation.record.namespace,
            repo_extra=operation.repo_extra,
            **connector_extra,
        )
        await connector.delete(
            storage_path=ctx.to_storage_path,
            repo_extra=operation.repo_extra,
        )
        operation.record.status = OperationStatusEnum.UPLOADED

    @staticmethod
    async def finalize(
        *,
        operation: OperationRecord,
        connector: AbstractConnector,
        **connector_extra,
    ):
        ctx: DeleteContext = operation.context
        await connector.delete(
            storage_path=ctx.to_storage_path,
            repo_extra=operation.repo_extra,
            **connector_extra,
        )
