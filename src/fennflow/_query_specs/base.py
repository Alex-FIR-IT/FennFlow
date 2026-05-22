from dataclasses import dataclass
from typing import Generic, TypeVar

ReturnType = TypeVar("ReturnType")


@dataclass(slots=True, frozen=True)
class BaseQuerySpec(Generic[ReturnType]):
    pass
