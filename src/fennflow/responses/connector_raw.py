from dataclasses import dataclass
from typing import Generic

from typing_extensions import TypeVar

ConnectorResponseT = TypeVar("ConnectorResponseT")


@dataclass(slots=True)
class ConnectorRawResponse(Generic[ConnectorResponseT]):
    raw_response: ConnectorResponseT
