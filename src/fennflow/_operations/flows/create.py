from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._operations.context.create import CreateContext
from fennflow._operations.enums import OperationStatusEnum
from fennflow._operations.flows.abstract import AbstractFlow
from fennflow._sentinel import OMIT

if TYPE_CHECKING:
    from fennflow._new_types import ConnectorExtra
    from fennflow._operations.dto import OperationRecord
    from fennflow.connectors._abstract import AbstractConnector


class CreateFlow(AbstractFlow[CreateContext]):
    @staticmethod
    async def execute(
        *,
        operation: OperationRecord[CreateContext],
        connector: AbstractConnector,
        connector_extra: ConnectorExtra = OMIT,
    ):

        return await connector.put(
            file=operation.require_context().file,
            repo_extra=operation.repo_extra,
            connector_extra=connector_extra,
        )

    @staticmethod
    async def compensate(
        *,
        operation: OperationRecord,
        connector: AbstractConnector,
    ):

        result = await connector.delete(
            storage_path=operation.record.storage_path,
            repo_extra=operation.repo_extra,
        )
        operation.record.status = OperationStatusEnum.FAILED
        return result

    @staticmethod
    async def finalize(
        *,
        operation: OperationRecord,
        connector: AbstractConnector,
    ):
        pass
