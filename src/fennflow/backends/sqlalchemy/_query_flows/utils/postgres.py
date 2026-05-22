from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._shared import unique_constraint

if TYPE_CHECKING:
    from sqlalchemy.dialects.postgresql import Insert

    from fennflow.backends.sqlalchemy import AbstractOperationRecordModel


def get_update_fields(
    insert_stmt: Insert,
    model: type[AbstractOperationRecordModel],
) -> dict:
    """Returns fields required to update an operation.

        **Example**::

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
    """
    return {
        col.name: insert_stmt.excluded[col.name]
        for col in model.__table__.columns
        if col.name not in unique_constraint and not col.primary_key
    }
