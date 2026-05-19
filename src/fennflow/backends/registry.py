from .in_memory import InMemoryBackendConfig
from .in_memory.factory import InMemoryBackendFactory

backend_registry = {
    InMemoryBackendConfig.__name__: InMemoryBackendFactory,
}
