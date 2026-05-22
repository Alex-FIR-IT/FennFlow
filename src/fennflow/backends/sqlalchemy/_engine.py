from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import make_url

from ._enums import Dialect

if TYPE_CHECKING:
    from . import AsyncEngine


def async_engine_factory(
    url: str,
    schema: str,
) -> AsyncEngine:
    from . import create_async_engine

    dialect = make_url(url)
    if Dialect.SQLITE in dialect.drivername:
        return create_async_engine(url)

    return create_async_engine(
        url,
        execution_options={
            "schema_translate_map": {
                None: schema,
            }
        },
    )
