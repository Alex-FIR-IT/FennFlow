from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fennflow._query_specs.select.base import SelectQuerySpec
from fennflow._sentinel import OMIT, Omittable
from fennflow.backends.responses import RecordPage

if TYPE_CHECKING:
    from uuid import UUID


@dataclass(slots=True, frozen=True)
class SelectVisibleQuerySpec(SelectQuerySpec[RecordPage]):
    prefix: str
    limit: int
    session_id: UUID
    continuation_token: Omittable[str] = OMIT
