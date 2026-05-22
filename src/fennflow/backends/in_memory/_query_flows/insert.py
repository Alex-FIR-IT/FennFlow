from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fennflow._query_specs.insert.insert import InsertQuerySpec
from fennflow.backends.enums import OnConflictDoEnum
from fennflow.backends.exceptions import (
    RecordAlreadyExistsInBackendException,
)
from fennflow.backends.in_memory._query_flows.base import BaseInMemoryBackendQueryFlow

if TYPE_CHECKING:
    from fennflow._operations.dto import Record


@dataclass(slots=True)
class InsertFlow(BaseInMemoryBackendQueryFlow[InsertQuerySpec, None]):
    async def run(
        self,
        query_spec: InsertQuerySpec,
    ) -> None:

        for record in query_spec.records:
            scoped_storage = self.storage.get(record.scope, {})
            storage_record = scoped_storage.get((record.namespace, record.storage_path))

            if storage_record is None:
                self.__set(record)
                continue

            # if (
            #     storage_record.is_pending
            #     and storage_record.session_id != record.session_id
            # ):
            #     raise RecordLockedException(storage_path=storage_record.storage_path)

            match query_spec.on_conflict:
                case OnConflictDoEnum.DO_NOTHING:
                    continue
                case OnConflictDoEnum.REPLACE:
                    self.__set(record)
                case OnConflictDoEnum.RAISE:
                    raise RecordAlreadyExistsInBackendException(
                        storage_path=record.storage_path,
                    )
                case _:
                    raise AssertionError("Unhandled conflict strategy.")

    def __set(self, record: Record) -> None:
        self.storage[record.scope][(record.namespace, record.storage_path)] = record
