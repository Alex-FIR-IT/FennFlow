from __future__ import annotations

from dataclasses import dataclass

from fennflow._query_specs.select.count import CountQuerySpec
from fennflow.backends.sqlalchemy._query_flows.base import (
    BaseSqlalchemyBackendQueryFlow,
)


@dataclass(slots=True)
class CountFlow(BaseSqlalchemyBackendQueryFlow[CountQuerySpec, int]):
    async def run(
        self,
        query_spec: CountQuerySpec,  # noqa: ARG002
    ) -> int:
        from fennflow.backends.sqlalchemy._base import func, select

        stmt = select(func.count()).select_from(self.adapter.orm_model)

        result = await self.session.execute(stmt)
        return result.scalar_one()
