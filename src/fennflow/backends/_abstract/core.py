from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar

from fennflow.backends.enums import OnConflictDoEnum

if TYPE_CHECKING:

    from fennflow._operations.dto import OperationRecord
    from fennflow._query_specs.delete.base import DeleteQuerySpec
    from fennflow._query_specs.select.base import SelectQuerySpec
    from fennflow._query_specs.update.base import UpdateQuerySpec


ReturnType = TypeVar("ReturnType")


class AbstractBackend(ABC):
    @abstractmethod
    async def select(self, query: SelectQuerySpec[ReturnType]) -> ReturnType: ...

    @abstractmethod
    async def insert(
        self,
        *records: OperationRecord,
        on_conflict: OnConflictDoEnum = OnConflictDoEnum.RAISE,
    ) -> None: ...

    @abstractmethod
    async def update(self, query: UpdateQuerySpec) -> None: ...

    @abstractmethod
    async def delete(self, query: DeleteQuerySpec) -> None: ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...

    @abstractmethod
    async def open(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...
