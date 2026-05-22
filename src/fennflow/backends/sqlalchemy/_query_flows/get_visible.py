from __future__ import annotations

from dataclasses import dataclass

from fennflow._operations.dto import Record
from fennflow._operations.enums import OperationStatusEnum
from fennflow._query_specs.select.get_visible import GetVisibleQuerySpec
from fennflow._shared import inserting_types
from fennflow.backends.sqlalchemy._query_flows.base import (
    BaseSqlalchemyBackendQueryFlow,
    )


@dataclass(slots=True)
class GetVisibleFlow(
    BaseSqlalchemyBackendQueryFlow[GetVisibleQuerySpec, Record | None],
    ):
    async def run(
            self,
            query_spec: GetVisibleQuerySpec,
            ) -> Record | None:
        from fennflow.backends.sqlalchemy._base import select

        model = self.adapter.orm_model

        stmt = (
            select(model)
            .where(
                model.scope == query_spec.scope,
                model.namespace == query_spec.namespace,
                model.storage_path == query_spec.storage_path,
                (
                        (model.status == OperationStatusEnum.UPLOADED)
                        | (
                                (model.status == OperationStatusEnum.PENDING)
                                & (model.session_id == query_spec.session_id)
                                & (model.operation_type.in_(inserting_types))
                        )
                ),
                )
            .limit(1)
        )
        result = await self.session.execute(stmt)
        orm_obj = result.scalars().first()
        if orm_obj is None:
            return None
        return self.adapter.from_orm(orm_obj)
