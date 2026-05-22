from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from fennflow._query_specs.base import BaseQuerySpec


ReturnType = TypeVar("ReturnType")


class AbstractBackend(ABC):
    @abstractmethod
    async def execute(
        self,
        query: BaseQuerySpec[ReturnType],
    ) -> ReturnType: ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...

    @abstractmethod
    async def open(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...
