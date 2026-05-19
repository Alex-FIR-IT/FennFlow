from dataclasses import dataclass

from fennflow._query_specs.select.base import SelectQuerySpec


@dataclass(slots=True, frozen=True)
class IsEmptyQuerySpec(SelectQuerySpec[bool]):
    pass
