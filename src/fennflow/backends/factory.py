from __future__ import annotations

from typing import TYPE_CHECKING

from .._sessions.in_memory import InMemorySessionBuffer
from .core import BackendOrchestrator
from .registry import backend_registry

if TYPE_CHECKING:
    from fennflow.backends.types.config import BackendConfig


class BackendFactory:
    """Factory for creating backends from config."""

    @staticmethod
    def from_config(config: BackendConfig) -> BackendOrchestrator:

        specific_backend_factory = backend_registry.get(config.__class__.__name__)
        if not specific_backend_factory:
            raise ValueError(f"Unknown backend for : {type(config)=}")

        backend = specific_backend_factory.from_config(
            config,
        )

        return BackendOrchestrator(
            backend_engine=backend,
            session_buffer=InMemorySessionBuffer(),
        )
