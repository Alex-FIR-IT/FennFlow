from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from fennflow.backends.abstract.core import AbstractBackend
from fennflow.backends.enums import OnConflictDoEnum
from fennflow.backends.exceptions import (
    RecordAlreadyExistsInBackendException,
    RecordLockedException,
)

if TYPE_CHECKING:
    from typing_extensions import Self

    from fennflow._operations.dto import OperationRecord
    from fennflow._query_specs.delete.base import DeleteQuerySpec
    from fennflow._query_specs.dispatcher import Dispatcher
    from fennflow._query_specs.select.base import SelectQuerySpec
    from fennflow._query_specs.update.base import UpdateQuerySpec
    from fennflow.backends import InMemoryBackendConfig
    from fennflow.backends.in_memory._types import (
        InMemoryStorageType,
        ScopedStorageType,
    )

ReturnType = TypeVar("ReturnType")


class InMemoryBackend(AbstractBackend):
    _instance: ClassVar[Self | None] = None
    _initialized: ClassVar[bool] = False

    def __new__(cls, *args, **kwargs):  # noqa: ARG004

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(
        self,
        dispatcher: Dispatcher,
        storage: InMemoryStorageType,
        config: InMemoryBackendConfig,
    ) -> None:
        if self.__class__._initialized:
            return

        self.storage = storage
        self.dispatcher = dispatcher
        self._config = config

        self.__class__._initialized = True

    @property
    def scoped_storage(self) -> ScopedStorageType:
        return self.storage[self._config.scope]

    async def select(self, query: SelectQuerySpec[ReturnType]) -> ReturnType:
        return await self.dispatcher.dispatch(query_spec=query)

    async def insert(
        self,
        *records: OperationRecord,
        on_conflict: OnConflictDoEnum = OnConflictDoEnum.RAISE,
    ) -> None:
        new_records = {}
        for record in records:
            storage_record = self.scoped_storage.get(record.storage_path)

            if storage_record is None:
                new_records[record.storage_path] = record
                continue

            if (
                storage_record.is_pending
                and storage_record.session_id != record.session_id
            ):
                raise RecordLockedException(storage_path=record.storage_path)

            match on_conflict:
                case OnConflictDoEnum.DO_NOTHING:
                    continue
                case OnConflictDoEnum.REPLACE:
                    new_records[record.storage_path] = record
                case OnConflictDoEnum.RAISE:
                    raise RecordAlreadyExistsInBackendException(
                        storage_path=record.storage_path,
                    )
                case _:
                    raise AssertionError("Unhandled conflict strategy.")

        self.scoped_storage.update(new_records)

    async def update(self, query: UpdateQuerySpec) -> None:
        return await self.dispatcher.dispatch(query_spec=query)

    async def delete(self, query: DeleteQuerySpec) -> None:
        return await self.dispatcher.dispatch(query_spec=query)

    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def open(self) -> None:
        pass

    async def close(self) -> None:
        pass

    def clear(self):
        self.scoped_storage.clear()
