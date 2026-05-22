from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic

from fennflow._query_specs._types import QuerySpecT_contra, ReturnType_co
from fennflow._query_specs.protocols import HasRunMethodProtocol

if TYPE_CHECKING:
    from fennflow.backends.sqlalchemy import AsyncSession
    from fennflow.backends.sqlalchemy._adapter import RecordOrmAdapter
    from fennflow.backends.sqlalchemy._enums import Dialect
    from fennflow.backends.sqlalchemy.config import SqlalchemyBackendConfig


@dataclass(slots=True)
class BaseSqlalchemyBackendQueryFlow(
    HasRunMethodProtocol[QuerySpecT_contra, ReturnType_co],
    Generic[QuerySpecT_contra, ReturnType_co],
):
    config: SqlalchemyBackendConfig
    session: AsyncSession
    adapter: RecordOrmAdapter
    dialect: Dialect | str
