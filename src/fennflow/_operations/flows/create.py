from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._operations.enums import OperationStatusEnum
from fennflow._operations.flows.abstract import AbstractFlow

if TYPE_CHECKING:
    from fennflow._operations.context.create import CreateContext
    from fennflow._operations.dto import OperationRecord
    from fennflow.connectors._abstract import AbstractConnector


class CreateFlow(AbstractFlow):
    @staticmethod
    async def execute(
        *,
        operation: OperationRecord,
        connector: AbstractConnector,
        **provider_extra,
    ):
        ctx: CreateContext = operation.context
        return await connector.put(
            file=ctx.file,
            repo_extra=operation.repo_extra,
            **provider_extra,
        )

    @staticmethod
    async def compensate(
        *,
        operation: OperationRecord,
        connector: AbstractConnector,
        **provider_extra,
    ):

        result = await connector.delete(
            storage_path=operation.record.storage_path,
            repo_extra=operation.repo_extra,
            **provider_extra,
        )
        operation.record.status = OperationStatusEnum.FAILED
        return result

    @staticmethod
    async def finalize(
        *,
        operation: OperationRecord,
        connector: AbstractConnector,
        **provider_extra,
    ):
        pass
