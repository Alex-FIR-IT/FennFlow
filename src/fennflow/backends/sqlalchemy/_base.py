# ruff: noqa: F401
import datetime
import uuid

from fennflow._datetime import AwareDatetime, now
from fennflow._new_types import BackendScope, Namespace, StoragePath

try:
    from sqlalchemy import (
        DateTime,
        String,
        Text,
        UniqueConstraint,
        Uuid,
        delete,
        exists,
        func,
        insert,
        inspect,
        make_url,
        select,
        text,
    )
    from sqlalchemy.dialects.postgresql import insert as pg_insert
    from sqlalchemy.ext.asyncio import (
        AsyncEngine,
        AsyncSession,
        async_sessionmaker,
        create_async_engine,
    )
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
except ImportError as _import_error:
    raise ImportError(
        "Please install the `sqlalchemy` package to use the sqlalchemy backend.",
    ) from _import_error


class BaseSqlalchemyModel(DeclarativeBase):
    """Base class for SQLAlchemy ORM models in the fennflow backend."""

    __abstract__ = True

    def model_dump(
        self,
    ) -> dict:
        state = inspect(self)
        return {c.key: getattr(self, c.key) for c in state.mapper.columns}

    @property
    def pk(self):
        """Returns the primary key of the model."""
        pk_columns = inspect(self.__class__).primary_key

        pk_values = tuple(getattr(self, col.key) for col in pk_columns)

        if len(pk_values) == 1:
            return pk_values[0]

        return pk_values


class AbstractOperationRecordModel(BaseSqlalchemyModel):
    """Abstract model for fennflow metadata table.

    Used:
    1) in _model.py to create concrete model with dynamic table name and schema.
    2) for annotations.
    """

    __abstract__ = True

    operation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False,
        index=True,
    )

    scope: Mapped[BackendScope] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    namespace: Mapped[Namespace] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    storage_path: Mapped[StoragePath] = mapped_column(
        String(2048),
        nullable=False,
    )

    operation_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )

    created_at: Mapped[AwareDatetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=now,
        index=True,
    )

    expired_at: Mapped[AwareDatetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: now() + datetime.timedelta(seconds=30),
        index=True,
    )

    error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
