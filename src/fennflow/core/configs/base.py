from typing_extensions import TypedDict

from fennflow.backends._types.config import BackendConfig
from fennflow.connectors._types.config import ConnectorConfig
from fennflow.reconciler import ReconcileConfig


class ConfigDict(TypedDict, total=False):
    """Configuration for a UnitOfWork instance.

    All fields are optional — if not provided, defaults are used.

    Attributes:
        backend: Configuration for the metadata backend
            (e.g. ``SqlalchemyBackendConfig``).
        connector: Configuration for the storage connector (e.g. ``S3ConnectorConfig``).

    Example::

        class UOW(UnitOfWork):
            config = ConfigDict(
                backend=SqlalchemyBackendConfig(),
                connector=S3ConnectorConfig(),

            )
    """

    backend: BackendConfig
    connector: ConnectorConfig
    reconcile: ReconcileConfig
