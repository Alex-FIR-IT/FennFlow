from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow.backends.enums import OnConflictDoEnum
from fennflow.backends.sqlalchemy._query_flows.utils.agnostic_upsert import upsert

if TYPE_CHECKING:
    from fennflow._query_specs.insert.insert import InsertQuerySpec
    from fennflow.backends.sqlalchemy._query_flows.insert.core import InsertFlow


async def run(
    flow: InsertFlow,
    query_spec: InsertQuerySpec,
) -> None:
    from fennflow.backends.sqlalchemy._base import insert

    records = query_spec.records
    model = flow.adapter.orm_model
    orm_instances = [flow.adapter.to_orm(record) for record in records]

    match query_spec.on_conflict:
        case OnConflictDoEnum.REPLACE:
            for orm_instance in orm_instances:
                await upsert(session=flow.session, orm_instance=orm_instance)
        case OnConflictDoEnum.DO_NOTHING:
            for orm_instance in orm_instances:
                existing = await flow.session.get(
                    model,
                    orm_instance.pk,
                    with_for_update=True,
                )
                if existing is None:
                    flow.session.add(orm_instance)

        case OnConflictDoEnum.RAISE:
            stmt = insert(model).values(
                tuple(orm_model.model_dump() for orm_model in orm_instances)
            )
            await flow.session.execute(stmt)
        case _:
            raise AssertionError(
                f"Unhandled conflict strategy: {query_spec.on_conflict}",
            )
