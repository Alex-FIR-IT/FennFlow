from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from typing_extensions import Self

from fennflow._query_specs.update.base import UpdateQuerySpec

if TYPE_CHECKING:
    from collections.abc import Iterable

    from fennflow._operations.dto import OperationRecord, Record


@dataclass(slots=True, frozen=True)
class MergeQuerySpec(UpdateQuerySpec[None]):
    """Used to merge multiple records into a single record.

    INSERT OR REPLACE INTO <table> (<record fields>)
    VALUES (<record values>), (<record values>), ...
    """

    records: Iterable[Record]

    @classmethod
    def from_operations(cls, operations: Iterable[OperationRecord]) -> Self:
        return cls(records=(op.record for op in operations))
