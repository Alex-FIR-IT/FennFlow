from fennflow.connectors._abstract.config import AbstractConnectorConfig


class InMemoryConnectorConfig(AbstractConnectorConfig):
    """Configuration for the in-memory connector.

    No configuration is required — the in-memory connector
    is zero-dependency and is intended for testing and development only.
    """
