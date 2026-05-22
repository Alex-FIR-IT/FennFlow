from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow.backends.sqlalchemy._query_flows.utils.agnostic_upsert import upsert

if TYPE_CHECKING:
    from fennflow._query_specs.insert.insert import InsertQuerySpec
    from fennflow.backends.sqlalchemy._query_flows.merge.core import MergeFlow


async def run(
    flow: MergeFlow,
    query_spec: InsertQuerySpec,
) -> None:
    rows = [flow.adapter.to_orm(record) for record in query_spec.records]

    for row in rows:
        await upsert(session=flow.session, orm_instance=row)
