from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._operations.context.abstract import BaseContext
from fennflow._sessions.abstract import AbstractSessionBuffer
from fennflow.backends.enums import OnConflictDoEnum
from fennflow.backends.exceptions import RecordAlreadyExistsInSessionException

if TYPE_CHECKING:
    from collections.abc import ValuesView

    from fennflow._new_types import StoragePath
    from fennflow._operations.dto import OperationRecord


class InMemorySessionBuffer(AbstractSessionBuffer):
    def __init__(self) -> None:
        self._operations: dict[StoragePath, OperationRecord] = {}

    def clear(self) -> None:
        for op in self._operations.values():
            op.context = BaseContext()

        self._operations.clear()

    def get(self, storage_path: StoragePath) -> OperationRecord | None:
        return self._operations.get(storage_path)

    def get_all(self) -> ValuesView[OperationRecord]:
        return self._operations.values()

    def add(
        self,
        *records: OperationRecord,
        on_conflict: OnConflictDoEnum,
    ) -> None:
        for record in records:
            storage_record = self.get(record.storage_path)

            if storage_record:
                match on_conflict:
                    case OnConflictDoEnum.DO_NOTHING:
                        continue
                    case OnConflictDoEnum.REPLACE:
                        self._set(record)
                    case OnConflictDoEnum.RAISE:
                        raise RecordAlreadyExistsInSessionException(
                            storage_path=record.storage_path,
                        )
                    case _:
                        raise AssertionError("Unhandled conflict strategy.")
            else:
                self._set(record)

    def _set(self, record: OperationRecord) -> None:
        self._operations[record.storage_path] = record
