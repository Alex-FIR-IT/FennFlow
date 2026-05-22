from fennflow._query_specs.base import BaseQuerySpec
from fennflow.backends.sqlalchemy._query_flows.base import (
    BaseSqlalchemyBackendQueryFlow,
)

QueryFlowRegistryType = dict[type[BaseQuerySpec], BaseSqlalchemyBackendQueryFlow]
