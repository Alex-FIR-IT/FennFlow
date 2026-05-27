from fennflow._base_exception import FennFlowException


class BaseConnectorException(FennFlowException):
    """Base exception for connector-related errors."""


class NoSuchKeyException(BaseConnectorException):
    """Raised when a requested key is not found in the connector storage."""

    def __init__(
        self,
        *args,
        msg: str = "The specified key does not exist.",
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)


class ConnectorCapabilityException(BaseConnectorException):
    """Raise when a connector does not support a capability."""

    def __init__(self, capability: str) -> None:
        msg = f"Connector does not support the capability - {capability}"
        super().__init__(msg)
        self.capability = capability
