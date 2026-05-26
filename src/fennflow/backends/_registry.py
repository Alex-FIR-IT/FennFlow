from .in_memory import InMemoryBackendConfig
from .sqlalchemy._factory import SqlalchemyBackendFactory
from .sqlalchemy.config import SqlalchemyBackendConfig

backend_registry = {
    InMemoryBackendConfig.__name__: SqlalchemyBackendFactory,
    SqlalchemyBackendConfig.__name__: SqlalchemyBackendFactory,
}
