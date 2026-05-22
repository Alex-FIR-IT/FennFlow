from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import insert

from fennflow.backends.enums import OnConflictDoEnum

if TYPE_CHECKING:
    from fennflow._query_specs.insert.insert import InsertQuerySpec
    from fennflow.backends.sqlalchemy._query_flows.insert.core import InsertFlow


async def run(
    flow: InsertFlow,
    query_spec: InsertQuerySpec,
) -> None:
    records = query_spec.records
    model = flow.adapter.orm_model
    rows = [flow.adapter.to_orm(record) for record in records]

    match query_spec.on_conflict:
        case OnConflictDoEnum.REPLACE:
            for row in rows:
                await flow.session.merge(row)
        case OnConflictDoEnum.DO_NOTHING:
            for row in rows:
                existing = await flow.session.get(model, row.pk, with_for_update=True)
                if existing is None:
                    flow.session.add(row)

        case OnConflictDoEnum.RAISE:
            stmt = insert(model).values(rows)
            await flow.session.execute(stmt)
        case _:
            raise AssertionError(
                f"Unhandled conflict strategy: {query_spec.on_conflict}"
            )
