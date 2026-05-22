from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

from typing_extensions import Self

from fennflow._query_specs.insert.base import BaseInsertQuerySpec
from fennflow.backends.enums import OnConflictDoEnum

if TYPE_CHECKING:
    from collections.abc import Iterable

    from fennflow._operations.dto import OperationRecord, Record

ReturnType = TypeVar("ReturnType")


@dataclass(slots=True, frozen=True)
class InsertQuerySpec(BaseInsertQuerySpec[None]):
    """Insert records into the fennflow metadata table.

    INSERT INTO <table>(<record fields>)
    VALUES (<record values>), (<record values>), ...
    ON CONFLICT <conflict target> DO <conflict action>;
    """

    records: Iterable[Record]
    on_conflict: OnConflictDoEnum = OnConflictDoEnum.RAISE

    @classmethod
    def from_operations(
        cls,
        operations: Iterable[OperationRecord],
        on_conflict: OnConflictDoEnum = OnConflictDoEnum.RAISE,
    ) -> Self:
        return cls(
            records=(op.record for op in operations),
            on_conflict=on_conflict,
        )
