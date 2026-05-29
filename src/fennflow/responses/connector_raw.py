from dataclasses import dataclass
from typing import Generic

from typing_extensions import TypeVar

ConnectorResponseT = TypeVar("ConnectorResponseT")


@dataclass(slots=True)
class ConnectorRawResponse(Generic[ConnectorResponseT]):
    """Wraps a raw response from a connector.

    Intended as a base class to provide original connector response.

    Type Parameters:
        ConnectorResponseT: The type of the raw connector response
            (e.g. aiobotocore GetObjectOutputTypeDef).

    """

    raw_response: ConnectorResponseT
    """The unprocessed response returned directly by the connector."""
