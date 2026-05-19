from __future__ import annotations

from itertools import groupby
from typing import TYPE_CHECKING

from typing_extensions import Self

from fennflow._operations.dto import OperationRecord
from fennflow._query_specs.select.get_by_storage_path import GetByStoragePathQuerySpec
from fennflow._query_specs.update.merge import MergeQuerySpec
from fennflow._sentinel import OMIT, Omittable, is_given
from fennflow.backends.enums import OnConflictDoEnum

if TYPE_CHECKING:
    from collections.abc import Iterable

    from fennflow._sessions.abstract import AbstractSessionBuffer
    from fennflow.backends.abstract.core import AbstractBackend


class BackendOrchestrator:
    def __init__(
        self,
        backend_engine: AbstractBackend,
        session_buffer: AbstractSessionBuffer,
    ):
        self.backend_engine = backend_engine
        self.session_buffer = session_buffer

    async def open(self) -> Self:
        await self.backend_engine.open()
        return self

    async def close(self):
        await self.backend_engine.close()

    async def get(self, storage_path) -> OperationRecord | None:
        session_obj = self.session_buffer.get(storage_path)

        if session_obj is not None:
            return session_obj

        backend_obj = await self.backend_engine.select(
            GetByStoragePathQuerySpec(storage_path=storage_path)
        )

        return backend_obj

    async def insert(
        self,
        records: OperationRecord | list[OperationRecord],
        on_conflict: OnConflictDoEnum = OnConflictDoEnum.RAISE,
    ) -> None:

        if isinstance(records, OperationRecord):
            records = [records]

        for record in records:
            record.on_conflict = on_conflict

        self.session_buffer.add(
            *records,
            on_conflict=on_conflict,
        )

    async def flush(
        self,
        operations: Omittable[Iterable[OperationRecord]] = OMIT,
    ) -> None:
        if not is_given(operations):
            operations = self.session_buffer.get_all()

        for on_conflict, batch in groupby(operations, lambda op: op.on_conflict):
            await self.backend_engine.insert(*batch, on_conflict=on_conflict)

        await self.backend_engine.commit()

    async def commit(self):
        operations = self.session_buffer.get_all()
        await self.backend_engine.update(MergeQuerySpec(operations=operations))
        await self.backend_engine.commit()
        self.session_buffer.clear()
