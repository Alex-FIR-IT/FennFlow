from __future__ import annotations

from dataclasses import dataclass

from fennflow._operations.enums import OperationStatusEnum
from fennflow._query_specs.select.select_visible import SelectVisibleQuerySpec
from fennflow._sentinel import is_given
from fennflow._shared import inserting_types
from fennflow.backends.responses import RecordPage
from fennflow.backends.sqlalchemy import select
from fennflow.backends.sqlalchemy._query_flows.base import (
    BaseSqlalchemyBackendQueryFlow,
)


@dataclass(slots=True)
class SelectVisibleFlow(
    BaseSqlalchemyBackendQueryFlow[SelectVisibleQuerySpec, RecordPage]
):
    async def run(
        self,
        query_spec: SelectVisibleQuerySpec,
    ) -> RecordPage:
        model = self.adapter.orm_model

        conditions = [
            model.scope == query_spec.scope,
            model.namespace == query_spec.namespace,
            model.storage_path.like(query_spec.prefix + "%"),
            (
                (model.status == OperationStatusEnum.UPLOADED)
                | (
                    (model.status == OperationStatusEnum.PENDING)
                    & (model.session_id == query_spec.session_id)
                    & (model.operation_type.in_(inserting_types))
                )
            ),
        ]

        if is_given(query_spec.continuation_token):
            conditions.append(model.storage_path > query_spec.continuation_token)

        stmt = (
            select(model)
            .where(*conditions)
            .order_by(model.storage_path.asc())
            .limit(query_spec.limit + 1)  # fetch one extra to detect next page
        )

        result = await self.session.execute(stmt)
        orm_objects = result.scalars().all()

        has_next = len(orm_objects) > query_spec.limit
        page_objects = orm_objects[: query_spec.limit]

        records = tuple(self.adapter.from_orm(obj) for obj in page_objects)
        next_token = page_objects[-1].storage_path if has_next else None

        return RecordPage(operations=records, continuation_token=next_token)
