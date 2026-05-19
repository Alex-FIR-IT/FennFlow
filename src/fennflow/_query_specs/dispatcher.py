from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fennflow._query_specs.base import BaseQuerySpec
    from fennflow._query_specs.protocols import HasRunMethodProtocol


class Dispatcher:
    def __init__(
        self,
        registry: dict[type[BaseQuerySpec], HasRunMethodProtocol],
    ) -> None:
        self.registry = registry

    async def dispatch(self, query_spec: BaseQuerySpec) -> Any:
        if type(query_spec) not in self.registry:
            raise KeyError(f"Query spec {type(query_spec)=} not found in registry.")
        handler = self.registry[type(query_spec)]
        return await handler.run(query_spec=query_spec)
