from dataclasses import dataclass

from fennflow._operations.dto import OperationRecord
from fennflow._query_specs.select.base import SelectQuerySpec


@dataclass(slots=True, frozen=True)
class GetByStoragePathQuerySpec(SelectQuerySpec[OperationRecord | None]):
    storage_path: str
