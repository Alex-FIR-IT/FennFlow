from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

from fennflow._query_specs.insert.base import BaseInsertQuerySpec

if TYPE_CHECKING:
    from collections.abc import Iterable

    from typing_extensions import Self

    from fennflow._operations.dto import OperationRecord, Record

ReturnType = TypeVar("ReturnType")


@dataclass(slots=True, frozen=True)
class MergeOutboxQuerySpec(BaseInsertQuerySpec[None]):
    """Insert or replace records into the fennflow outbox table.

    INSERT OR REPLACE INTO <table>(<record fields>)
    VALUES (<record values>), (<record values>), ...
    ON CONFLICT <conflict target> DO <conflict action>;
    """

    records: Iterable[Record]

    @classmethod
    def from_operations(
        cls,
        operations: Iterable[OperationRecord],
    ) -> Self:
        return cls(
            records=(op.record for op in operations),
        )
