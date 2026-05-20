from dataclasses import dataclass

from fennflow._operations.dto import Record
from fennflow._query_specs.select.base import SelectQuerySpec


@dataclass(slots=True, frozen=True)
class GetByStoragePathQuerySpec(SelectQuerySpec[Record | None]):
    storage_path: str
