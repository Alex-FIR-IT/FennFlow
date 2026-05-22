from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as pg_insert

from fennflow._shared import unique_constraint
from fennflow.backends.enums import OnConflictDoEnum
from fennflow.backends.sqlalchemy._query_flows.utils.postgres import get_update_fields

if TYPE_CHECKING:
    from fennflow._query_specs.insert.insert import InsertQuerySpec
    from fennflow.backends.sqlalchemy._query_flows.insert.core import InsertFlow


async def run(
    flow: InsertFlow,
    query_spec: InsertQuerySpec,
) -> None:
    rows = tuple(flow.adapter.to_orm(r).model_dump() for r in query_spec.records)

    model = flow.adapter.orm_model

    match query_spec.on_conflict:
        case OnConflictDoEnum.RAISE:
            stmt = insert(model).values(rows)

        case OnConflictDoEnum.DO_NOTHING:
            stmt = pg_insert(model).values(rows).on_conflict_do_nothing()

        case OnConflictDoEnum.REPLACE:
            insert_stmt = pg_insert(model).values(rows)
            stmt = insert_stmt.on_conflict_do_update(
                index_elements=unique_constraint,
                set_=get_update_fields(insert_stmt=insert_stmt, model=model),
            )
        case _:
            raise AssertionError(
                f"Unhandled conflict strategy: {query_spec.on_conflict}"
            )
    await flow.session.execute(stmt)
