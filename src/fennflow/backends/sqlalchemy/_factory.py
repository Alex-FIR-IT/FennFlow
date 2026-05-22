from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._query_specs.delete.delete_scope import DeleteScopeQuerySpec
from fennflow._query_specs.insert.insert import InsertQuerySpec
from fennflow._query_specs.select.get_by_storage_path import GetByStoragePathQuerySpec
from fennflow._query_specs.select.get_visible import GetVisibleQuerySpec
from fennflow._query_specs.select.is_empty import IsEmptyQuerySpec
from fennflow._query_specs.select.select_visible import SelectVisibleQuerySpec
from fennflow._query_specs.update.merge import MergeQuerySpec
from fennflow.backends.sqlalchemy._core import SqlalchemyBackend
from fennflow.backends.sqlalchemy._query_flows.delete_scope import DeleteScopeFlow
from fennflow.backends.sqlalchemy._query_flows.get_by_storage_path import (
    GetByStoragePathFlow,
)
from fennflow.backends.sqlalchemy._query_flows.get_visible import GetVisibleFlow
from fennflow.backends.sqlalchemy._query_flows.insert.core import InsertFlow
from fennflow.backends.sqlalchemy._query_flows.is_empty import IsEmptyFlow
from fennflow.backends.sqlalchemy._query_flows.merge.core import MergeFlow
from fennflow.backends.sqlalchemy._query_flows.select_visible import SelectVisibleFlow

if TYPE_CHECKING:
    from fennflow.backends.sqlalchemy import AsyncSession
    from fennflow.backends.sqlalchemy._adapter import RecordOrmAdapter
    from fennflow.backends.sqlalchemy._enums import Dialect
    from fennflow.backends.sqlalchemy._types import (
        QueryFlowRegistryType,
    )
    from fennflow.backends.sqlalchemy.config import SqlalchemyBackendConfig


class SqlalchemyBackendFactory:
    @staticmethod
    def _create_registry(
        config: SqlalchemyBackendConfig,
        session: AsyncSession,
        dialect: Dialect | str,
        adapter: RecordOrmAdapter,
    ) -> QueryFlowRegistryType:
        spec_to_flow = (
            (SelectVisibleQuerySpec, SelectVisibleFlow),
            (GetByStoragePathQuerySpec, GetByStoragePathFlow),
            (GetVisibleQuerySpec, GetVisibleFlow),
            (IsEmptyQuerySpec, IsEmptyFlow),
            (MergeQuerySpec, MergeFlow),
            (InsertQuerySpec, InsertFlow),
            (DeleteScopeQuerySpec, DeleteScopeFlow),
        )
        return {
            query_spec: flow(
                config=config,
                session=session,
                dialect=dialect,
                adapter=adapter,
            )
            for query_spec, flow in spec_to_flow
        }

    @classmethod
    def from_config(
        cls,
        config: SqlalchemyBackendConfig,
    ) -> SqlalchemyBackend:
        return SqlalchemyBackend(config=config)
