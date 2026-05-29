from dataclasses import KW_ONLY, dataclass
from typing import Generic

from typing_extensions import TypeVar

from .list import ListResponse

ConnectorResponseT = TypeVar("ConnectorResponseT")


@dataclass(slots=True)
class ConnectorListResponse(
    ListResponse,
    Generic[ConnectorResponseT],
):
    _: KW_ONLY
    raw_response: ConnectorResponseT
