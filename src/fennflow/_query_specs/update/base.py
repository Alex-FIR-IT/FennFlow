from dataclasses import dataclass
from typing import Generic, TypeVar

from fennflow._query_specs.base import BaseQuerySpec

ReturnType = TypeVar("ReturnType")


@dataclass(slots=True, frozen=True)
class UpdateQuerySpec(BaseQuerySpec[ReturnType], Generic[ReturnType]):
    pass
