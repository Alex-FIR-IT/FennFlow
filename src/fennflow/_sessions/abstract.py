from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from fennflow._new_types import StoragePath
    from fennflow._operations.dto import OperationRecord
    from fennflow.backends.enums import OnConflictDoEnum


class AbstractSessionBuffer(ABC):
    @abstractmethod
    def add(
        self,
        *records: OperationRecord,
        on_conflict: OnConflictDoEnum,
    ) -> None: ...

    @abstractmethod
    def get(self, storage_path: StoragePath) -> OperationRecord | None: ...

    @abstractmethod
    def get_all(self) -> Iterable[OperationRecord]: ...

    @abstractmethod
    def clear(self) -> None: ...
