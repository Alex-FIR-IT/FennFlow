from typing import TypeAlias

from fennflow.backends.in_memory import InMemoryBackendConfig
from fennflow.backends.sqlalchemy.config import SqlalchemyBackendConfig

BackendConfig: TypeAlias = InMemoryBackendConfig | SqlalchemyBackendConfig
