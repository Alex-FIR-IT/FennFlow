from pydantic import Field

from fennflow.backends._abstract.config import AbstractBackendConfig


class SqlalchemyBackendConfig(AbstractBackendConfig):
    """Configuration for the SqlAlchemy backend.

    No configuration is required — the in-memory backend
    is zero-dependency.
    """

    database_url: str = Field(
        default="sqlite+aiosqlite:///fennflow.db",
        description="Database URL for the FennFlow database",
    )
    db_schema: str = Field(
        default="fennflow",
        description="Schema for the FennFlow database",
    )
    table_name: str = Field(
        default="metadata",
        description="Table name for the FennFlow metadata records",
    )
