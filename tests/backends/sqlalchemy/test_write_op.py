from __future__ import annotations

import contextlib

import pytest
from sqlalchemy.exc import IntegrityError

from fennflow._query_specs.insert.insert import InsertQuerySpec
from fennflow._query_specs.select.count import CountQuerySpec
from fennflow._query_specs.update.merge import MergeQuerySpec
from fennflow.backends.enums import OnConflictDoEnum
from fennflow.backends.sqlalchemy._enums import Dialect
from fennflow.backends.sqlalchemy._query_flows.insert.core import InsertFlow
from fennflow.backends.sqlalchemy._query_flows.merge.core import MergeFlow
from tests.conftest import TestSqliteUOW


@pytest.fixture
def uow_cls():
    return TestSqliteUOW


def get_insert_flow(uow, dialect: Dialect) -> InsertFlow:
    return InsertFlow(
        config=uow._resolved_config.backend,
        adapter=uow.backend.backend_engine._adapter,
        dialect=dialect,
        session=uow.backend.backend_engine.session,
    )


def get_merge_flow(uow, dialect: Dialect) -> MergeFlow:
    return MergeFlow(
        config=uow._resolved_config.backend,
        adapter=uow.backend.backend_engine._adapter,
        dialect=dialect,
        session=uow.backend.backend_engine.session,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("dialect", [Dialect.SQLITE, "another_unhandled_dialect"])
@pytest.mark.parametrize("on_conflict", [value for value in OnConflictDoEnum])
async def test_insert_and_merge(uow_cls, dialect, operations, on_conflict):
    async with uow_cls() as uow:
        insert_flow = get_insert_flow(uow, dialect)
        merge_flow = get_merge_flow(uow, dialect)

        await insert_flow.run(
            InsertQuerySpec.from_operations(
                operations=operations[:6],
                on_conflict=on_conflict,
            )
        )
        await merge_flow.run(
            MergeQuerySpec.from_operations(
                operations=operations[4:],
            )
        )
        await uow.backend.backend_engine.commit()
        count_result = await uow.backend.backend_engine.execute(CountQuerySpec())

        assert count_result == len(operations)


@pytest.mark.asyncio
@pytest.mark.parametrize("dialect", [Dialect.SQLITE, "another_unhandled_dialect"])
@pytest.mark.parametrize(
    "on_conflict, expected_context, get_expected_count",
    [
        pytest.param(
            OnConflictDoEnum.DO_NOTHING,
            contextlib.nullcontext(),
            len,
            id="do_nothing",
        ),
        pytest.param(
            OnConflictDoEnum.REPLACE,
            contextlib.nullcontext(),
            len,
            id="replace",
        ),
        pytest.param(
            OnConflictDoEnum.RAISE,
            pytest.raises(IntegrityError),
            lambda ops: len(ops[4:]),
            id="raise",
        ),
    ],
)
async def test_merge_and_insert(
    uow_cls, dialect, operations, on_conflict, expected_context, get_expected_count
):
    async with uow_cls() as uow:
        insert_flow = get_insert_flow(uow, dialect)
        merge_flow = get_merge_flow(uow, dialect)

        await merge_flow.run(
            MergeQuerySpec.from_operations(
                operations=operations[4:],
            )
        )

        with expected_context:
            await insert_flow.run(
                InsertQuerySpec.from_operations(
                    operations=operations[:6],
                    on_conflict=on_conflict,
                )
            )

        await uow.backend.backend_engine.commit()
        count_result = await uow.backend.backend_engine.execute(CountQuerySpec())

        assert count_result == get_expected_count(operations)
