from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from fennflow._fallback_registry import FallbackRegistry
from fennflow._query_specs.update.merge import MergeQuerySpec
from fennflow._query_specs.update.outbox import MergeOutboxQuerySpec
from fennflow.backends.sqlalchemy._enums import Dialect
from fennflow.backends.sqlalchemy._query_flows.base import (
    BaseSqlalchemyBackendQueryFlow,
)

from . import db_agnostic, postgres

MergeFlowStrategy = Callable[
    ["MergeFlow", MergeQuerySpec],
    Awaitable[None],
]

fallback_registry = FallbackRegistry[
    Dialect | str,
    MergeFlowStrategy,
    MergeFlowStrategy,
](
    registry={
        Dialect.POSTGRES: postgres.run,
        Dialect.SQLITE: postgres.run,
    },
    default_value=db_agnostic.run,
)


@dataclass(slots=True)
class MergeFlow(BaseSqlalchemyBackendQueryFlow[MergeQuerySpec, None]):
    async def run(
        self,
        query_spec: MergeQuerySpec,
    ) -> None:
        flow = fallback_registry[self.dialect]
        return await flow(self, query_spec)


@dataclass(slots=True)
class MergeOutboxFlow(BaseSqlalchemyBackendQueryFlow[MergeOutboxQuerySpec, None]):
    async def run(
        self,
        query_spec: MergeOutboxQuerySpec,
    ):
        return await db_agnostic.run(self, query_spec)
