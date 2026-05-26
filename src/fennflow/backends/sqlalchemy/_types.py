from typing_extensions import TypeAliasType

from fennflow._query_specs.base import BaseQuerySpec
from fennflow.backends.sqlalchemy._query_flows.base import (
    BaseSqlalchemyBackendQueryFlow,
)

QueryFlowRegistryType = dict[type[BaseQuerySpec], BaseSqlalchemyBackendQueryFlow]

DatabaseUrl = TypeAliasType("DatabaseUrl", str)
Schema = TypeAliasType("Schema", str)
EngineRegistryKey = tuple[DatabaseUrl, Schema]
