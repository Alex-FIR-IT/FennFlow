from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Any

    from fennflow._query_specs.base import BaseQuerySpec


class HasRunMethodProtocol(Protocol):
    async def run(self, query_spec: BaseQuerySpec) -> Any: ...
