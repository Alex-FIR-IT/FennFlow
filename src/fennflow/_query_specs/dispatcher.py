from __future__ import annotations

from typing import TYPE_CHECKING, Generic

from fennflow._query_specs.base import ReturnType

if TYPE_CHECKING:
    from collections.abc import Mapping

    from fennflow._query_specs.base import BaseQuerySpec
    from fennflow._query_specs.protocols import HasRunMethodProtocol


class Dispatcher(Generic[ReturnType]):
    def __init__(
        self,
        registry: Mapping[type[BaseQuerySpec[ReturnType]], HasRunMethodProtocol],
    ) -> None:
        self.registry = registry

    async def dispatch(self, query_spec: BaseQuerySpec[ReturnType]) -> ReturnType:
        if type(query_spec) not in self.registry:
            raise KeyError(f"Query spec {type(query_spec)=} not found in registry.")
        handler = self.registry[type(query_spec)]
        return await handler.run(query_spec=query_spec)
