from __future__ import annotations

from typing import Generic, Protocol

from fennflow._query_specs._types import QuerySpecT_contra, ReturnType_co


class HasRunMethodProtocol(Protocol, Generic[QuerySpecT_contra, ReturnType_co]):
    async def run(self, query_spec: QuerySpecT_contra) -> ReturnType_co: ...
