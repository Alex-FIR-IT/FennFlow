from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from fennflow._fallback_registry import FallbackRegistry
from fennflow._query_specs.insert.insert import InsertQuerySpec
from fennflow.backends.sqlalchemy._enums import Dialect
from fennflow.backends.sqlalchemy._query_flows.base import (
    BaseSqlalchemyBackendQueryFlow,
)

from . import db_agnostic, postgres

InsertFlowStrategy = Callable[
    ["InsertFlow", InsertQuerySpec],
    Awaitable[None],
]

fallback_registry = FallbackRegistry[
    Dialect | str,
    InsertFlowStrategy,
    InsertFlowStrategy,
](
    registry={
        Dialect.POSTGRES: postgres.run,
        Dialect.SQLITE: postgres.run,
        },
    default_value=db_agnostic.run,
    )


@dataclass(slots=True)
class InsertFlow(BaseSqlalchemyBackendQueryFlow[InsertQuerySpec, None]):
    async def run(
            self,
            query_spec: InsertQuerySpec,
            ) -> None:
        flow = fallback_registry[self.dialect]
        return await flow(self, query_spec)
