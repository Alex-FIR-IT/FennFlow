from dataclasses import dataclass

from fennflow._query_specs.base import BaseQuerySpec


@dataclass(slots=True, frozen=True)
class DeleteQuerySpec(BaseQuerySpec):
    pass
