from .in_memory import InMemoryBackendConfig
from .in_memory._factory import InMemoryBackendFactory

backend_registry = {
    InMemoryBackendConfig.__name__: InMemoryBackendFactory,
}
