from __future__ import annotations

from pydantic import Field

from fennflow.backends.sqlalchemy.config import SqlalchemyBackendConfig


class InMemoryBackendConfig(SqlalchemyBackendConfig):
    """Configuration for the in-memory SQLite backend."""

    database_url: str = Field(
        default="sqlite+aiosqlite:///file:memdb1?mode=memory",
        description="Database URL for the in-memory SQLite database",
    )
