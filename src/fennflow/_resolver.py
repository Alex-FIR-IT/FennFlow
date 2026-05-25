from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fennflow.backends import SqlalchemyBackendConfig
from fennflow.connectors import S3ConnectorConfig
from fennflow.reconciler import (
    ReconcileConfig,
)

if TYPE_CHECKING:
    from fennflow import ConfigDict
    from fennflow.backends._types.config import BackendConfig
    from fennflow.connectors._types.config import ConnectorConfig


@dataclass(slots=True)
class ResolvedConfig:
    backend: BackendConfig
    connector: ConnectorConfig
    reconcile: ReconcileConfig


class ConfigResolver:
    @classmethod
    def resolve_config(
        cls,
        config: ConfigDict | None,
    ) -> ResolvedConfig:
        cfg = config or {}

        return ResolvedConfig(
            backend=cfg.get("backend") or SqlalchemyBackendConfig(),
            connector=cfg.get("connector") or S3ConnectorConfig(),
            reconcile=cfg.get("reconcile") or ReconcileConfig(),
        )
