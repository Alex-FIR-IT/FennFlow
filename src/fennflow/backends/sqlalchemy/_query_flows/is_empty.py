from __future__ import annotations

from dataclasses import dataclass

from fennflow._query_specs.select.is_empty import IsEmptyQuerySpec
from fennflow.backends.sqlalchemy import exists, select
from fennflow.backends.sqlalchemy._query_flows.base import (
    BaseSqlalchemyBackendQueryFlow,
)


@dataclass(slots=True)
class IsEmptyFlow(BaseSqlalchemyBackendQueryFlow[IsEmptyQuerySpec, bool]):
    async def run(
        self,
        query_spec: IsEmptyQuerySpec,
    ) -> bool:
        model = self.adapter.orm_model
        stmt = select(~exists().where(model.scope == query_spec.scope))
        result = await self.session.execute(stmt)
        return bool(result.scalar())
