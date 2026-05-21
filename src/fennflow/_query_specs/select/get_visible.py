from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fennflow._operations.dto import Record
from fennflow._query_specs.select.base import SelectQuerySpec

if TYPE_CHECKING:
    from uuid import UUID

    from fennflow._new_types import BackendScope, Namespace, StoragePath


@dataclass(slots=True, frozen=True)
class GetVisibleQuerySpec(SelectQuerySpec[Record | None]):
    storage_path: StoragePath
    session_id: UUID
