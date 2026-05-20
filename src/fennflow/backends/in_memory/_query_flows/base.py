from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic

from fennflow._query_specs._types import QuerySpecT_contra, ReturnType_co
from fennflow._query_specs.protocols import HasRunMethodProtocol

if TYPE_CHECKING:
    from fennflow.backends import InMemoryBackendConfig
    from fennflow.backends.in_memory._types import (
        InMemoryStorageType,
        ScopedStorageType,
    )


@dataclass(slots=True)
class BaseInMemoryBackendQueryFlow(
    HasRunMethodProtocol[QuerySpecT_contra, ReturnType_co],
    Generic[QuerySpecT_contra, ReturnType_co],
):
    storage: InMemoryStorageType
    config: InMemoryBackendConfig

    @property
    def scoped_storage(self) -> ScopedStorageType:
        return self.storage[self.config.scope]
