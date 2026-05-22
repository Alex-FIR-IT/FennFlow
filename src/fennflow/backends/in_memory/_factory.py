from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from fennflow._query_specs.delete.delete_scope import DeleteScopeQuerySpec
from fennflow._query_specs.dispatcher import Dispatcher
from fennflow._query_specs.insert.insert import InsertQuerySpec
from fennflow._query_specs.select.get_by_storage_path import GetByStoragePathQuerySpec
from fennflow._query_specs.select.get_visible import GetVisibleQuerySpec
from fennflow._query_specs.select.is_empty import IsEmptyQuerySpec
from fennflow._query_specs.select.select_visible import SelectVisibleQuerySpec
from fennflow._query_specs.update.merge import MergeQuerySpec
from fennflow.backends.in_memory._core import InMemoryBackend
from fennflow.backends.in_memory._query_flows.delete_scope import DeleteScopeFlow
from fennflow.backends.in_memory._query_flows.get_by_storage_path import (
    GetByStoragePathFlow,
)
from fennflow.backends.in_memory._query_flows.get_visible import GetVisibleFlow
from fennflow.backends.in_memory._query_flows.insert import InsertFlow
from fennflow.backends.in_memory._query_flows.is_empty import IsEmptyFlow
from fennflow.backends.in_memory._query_flows.merge import MergeFlow
from fennflow.backends.in_memory._query_flows.select_visible import SelectVisibleFlow

if TYPE_CHECKING:
    from fennflow.backends import InMemoryBackendConfig
    from fennflow.backends.in_memory._types import (
        InMemoryStorageType,
        QueryFlowRegistryType,
    )


class InMemoryBackendFactory:
    @staticmethod
    def _create_registry(
        config: InMemoryBackendConfig,
        storage: InMemoryStorageType,
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
                storage=storage,
            )
            for query_spec, flow in spec_to_flow
        }

    @classmethod
    def from_config(
        cls,
        config: InMemoryBackendConfig,
    ) -> InMemoryBackend:
        storage: InMemoryStorageType = defaultdict(dict)
        dispatcher: Dispatcher = Dispatcher(
            registry=cls._create_registry(
                config=config,
                storage=storage,
            )
        )
        return InMemoryBackend(
            dispatcher=dispatcher,
            storage=storage,
            config=config,
        )
