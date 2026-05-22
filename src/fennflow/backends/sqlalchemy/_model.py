from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow.backends.sqlalchemy._enums import Dialect

if TYPE_CHECKING:
    from typing import Any

    from sqlalchemy.ext.asyncio import AsyncEngine

    from fennflow.backends.sqlalchemy._base import AbstractOperationRecordModel

_MODEL_CACHE: dict[str, type[AbstractOperationRecordModel]] = {}


def create_operation_record_model(
        table_name: str,
        dialect: str | Dialect,
        schema: str | None = None,
        ) -> type[AbstractOperationRecordModel]:
    from ._base import (
        AbstractOperationRecordModel,
        UniqueConstraint,
        )

    if table_name in _MODEL_CACHE:
        return _MODEL_CACHE[table_name]

    model_name = f"{table_name.title().replace('_', '')}Model"

    table_args: list[Any] = [
        UniqueConstraint(
            "scope",
            "namespace",
            "storage_path",
            name=f"uq_{table_name}_scope_namespace_storage_path",
            ),
        ]

    if schema and dialect != Dialect.SQLITE:
        table_args.append({"schema": schema})

    _MODEL_CACHE[table_name] = type(
        model_name,
        (AbstractOperationRecordModel,),
        {
            "__tablename__": table_name,
            "__table_args__": tuple(table_args),
            },
        )
    return _MODEL_CACHE[table_name]


async def create_all(
        engine: AsyncEngine,
        schema: str | None = None,
        ) -> None:
    from ._base import BaseSqlalchemyModel, text

    async with engine.begin() as conn:
        if schema and conn.dialect.name != "sqlite":
            await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))

        await conn.run_sync(BaseSqlalchemyModel.metadata.create_all)
