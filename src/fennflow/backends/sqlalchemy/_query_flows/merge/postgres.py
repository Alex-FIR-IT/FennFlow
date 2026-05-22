from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql import insert as pg_insert

from fennflow._shared import unique_constraint
from fennflow.backends.sqlalchemy._query_flows.utils.postgres import get_update_fields

if TYPE_CHECKING:
    from fennflow._query_specs.insert.insert import InsertQuerySpec
    from fennflow.backends.sqlalchemy._query_flows.merge.core import MergeFlow


async def run(
    flow: MergeFlow,
    query_spec: InsertQuerySpec,
) -> None:
    rows = tuple(flow.adapter.to_orm(r).model_dump() for r in query_spec.records)

    model = flow.adapter.orm_model
    insert_stmt = pg_insert(model).values(rows)

    stmt = insert_stmt.on_conflict_do_update(
        index_elements=unique_constraint,
        set_=get_update_fields(
            insert_stmt=insert_stmt,
            model=model,
        ),
    )

    await flow.session.execute(stmt)
