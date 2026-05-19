from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fennflow._query_specs.update.base import UpdateQuerySpec

if TYPE_CHECKING:
    from collections.abc import Iterable

    from fennflow._operations.dto import OperationRecord


@dataclass(slots=True, frozen=True)
class MergeQuerySpec(UpdateQuerySpec):
    operations: Iterable[OperationRecord]
