from pydantic import Field

from fennflow.backends._abstract.config import AbstractBackendConfig


def database_url_factory() -> str:
    """Factory for database URL.

    Returns: str - representing aiosqlite URL
    Raises: ValueError - if aiosqlite is not installed
    """
    try:
        import aiosqlite  # noqa: F401
    except ImportError as _import_error:
        raise ValueError(
            "You need to pass database_url explicitly or "
            "install aiosqlite first - `pip install aiosqlite`"
        ) from _import_error

    return "sqlite+aiosqlite:///fennflow.db"


class SqlalchemyBackendConfig(AbstractBackendConfig):
    """Configuration for the SqlAlchemy backend.

    No configuration is required — the in-memory backend
    is zero-dependency.
    """

    database_url: str = Field(
        default_factory=database_url_factory,
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
