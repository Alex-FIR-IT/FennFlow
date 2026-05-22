from dataclasses import dataclass

from fennflow._query_specs.delete.delete_scope import DeleteScopeQuerySpec
from fennflow.backends.sqlalchemy._query_flows.base import (
    BaseSqlalchemyBackendQueryFlow,
    )


@dataclass(slots=True)
class DeleteScopeFlow(BaseSqlalchemyBackendQueryFlow[DeleteScopeQuerySpec, None]):
    async def run(
            self,
            query_spec: DeleteScopeQuerySpec,
            ) -> None:
        from fennflow.backends.sqlalchemy._base import delete

        model = self.adapter.orm_model

        stmt = delete(model).where(model.scope == query_spec.scope)
        await self.session.execute(stmt)
