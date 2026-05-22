from .in_memory import InMemoryBackendConfig
from .in_memory._factory import InMemoryBackendFactory
from .sqlalchemy._factory import SqlalchemyBackendFactory
from .sqlalchemy.config import SqlalchemyBackendConfig

backend_registry = {
    InMemoryBackendConfig.__name__: InMemoryBackendFactory,
    SqlalchemyBackendConfig.__name__: SqlalchemyBackendFactory,
}
