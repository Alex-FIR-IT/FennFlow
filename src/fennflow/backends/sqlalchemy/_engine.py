from __future__ import annotations

from typing import TYPE_CHECKING

from ._enums import Dialect

if TYPE_CHECKING:
    from ._base import AsyncEngine


def async_engine_factory(
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
