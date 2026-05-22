from dataclasses import dataclass

from fennflow._operations.dto import Record
from fennflow._query_specs.select.get_by_storage_path import GetByStoragePathQuerySpec
from fennflow.backends.sqlalchemy import select
from fennflow.backends.sqlalchemy._query_flows.base import (
    BaseSqlalchemyBackendQueryFlow,
)


@dataclass(slots=True)
class GetByStoragePathFlow(
    BaseSqlalchemyBackendQueryFlow[GetByStoragePathQuerySpec, Record | None]
):
    async def run(
        self,
        query_spec: GetByStoragePathQuerySpec,
    ) -> Record | None:

        model = self.adapter.orm_model
        stmt = (
            select(model)
            .where(
                model.scope == query_spec.scope,
                model.namespace == query_spec.namespace,
                model.storage_path == query_spec.storage_path,
            )
            .limit(1)
        )
        result = await self.session.execute(stmt)
        orm_obj = result.scalars().first()
        if orm_obj is None:
            return None
        return self.adapter.from_orm(orm_obj)
