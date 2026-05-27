from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from fennflow._operations.context.abstract import BaseContext

if TYPE_CHECKING:
    from fennflow._operations.dto import OperationRecord
    from fennflow.connectors._abstract import AbstractConnector

ContextType = TypeVar("ContextType", bound=BaseContext)


class AbstractFlow(ABC, Generic[ContextType]):
    @staticmethod
    @abstractmethod
    async def execute(
        *,
        operation: OperationRecord[ContextType],
        connector: AbstractConnector,
        **connector_extra,
    ): ...

    @staticmethod
    @abstractmethod
    async def compensate(
        *,
        operation: OperationRecord[ContextType],
        connector: AbstractConnector,
    ): ...

    @staticmethod
    @abstractmethod
    async def finalize(
        *,
        operation: OperationRecord[ContextType],
        connector: AbstractConnector,
    ): ...
