from __future__ import annotations

import asyncio
import atexit
from typing import TYPE_CHECKING

from fennflow.backends.sqlalchemy._enums import Dialect

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine

    from fennflow.backends.sqlalchemy._types import (
        DatabaseUrl,
        EngineRegistryKey,
        Schema,
    )


class EngineManager:
    def __init__(self) -> None:
        self._engine_cache: dict[EngineRegistryKey, AsyncEngine] = {}

    def get(
        self,
        url: DatabaseUrl,
        schema: Schema,
    ) -> AsyncEngine:

        if self._engine_cache.get((url, schema)) is None:
            engine = self._create_async_engine(url, schema)
            self._register_engine(url, schema, engine)

        return self._engine_cache[(url, schema)]

    def _register_engine(self, url: DatabaseUrl, schema: Schema, engine) -> None:
        self._engine_cache[(url, schema)] = engine
        atexit.register(lambda: asyncio.run(engine.dispose()))

    @staticmethod
    def _create_async_engine(
        url: str,
        schema: str,
    ) -> AsyncEngine:
        from ._base import create_async_engine, make_url

        dialect = make_url(url)
        if Dialect.SQLITE in dialect.drivername:
            return create_async_engine(url)

        return create_async_engine(
            url,
            execution_options={
                "schema_translate_map": {
                    None: schema,
                },
            },
        )


engine_manager = EngineManager()
