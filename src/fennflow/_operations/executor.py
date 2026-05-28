from __future__ import annotations

from typing import TYPE_CHECKING

from .._sentinel import OMIT
from .registry import flow_registry

if TYPE_CHECKING:
    from fennflow.connectors._abstract import AbstractConnector

    from .._new_types import ConnectorExtra
    from .dto import OperationRecord


class OperationExecutor:
    def __init__(self, connector: AbstractConnector) -> None:
        self.connector = connector

    async def execute(
        self,
        operation: OperationRecord,
        connector_extra: ConnectorExtra = OMIT,
    ):
        operation_flow = flow_registry[operation.record.operation_type]
        return await operation_flow().execute(
            operation=operation,
            connector=self.connector,
            connector_extra=connector_extra,
        )

    async def compensate(
        self,
        operation: OperationRecord,
    ):
        operation_flow = flow_registry[operation.record.operation_type]
        return await operation_flow().compensate(
            operation=operation,
            connector=self.connector,
        )

    async def finalize(
        self,
        operation: OperationRecord,
    ):
        operation_flow = flow_registry[operation.record.operation_type]
        return await operation_flow().finalize(
            operation=operation,
            connector=self.connector,
        )
