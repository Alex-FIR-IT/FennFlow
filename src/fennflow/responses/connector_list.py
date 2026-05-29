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
    """Extends ListResponse with the raw connector response.

    Returned by connector list operations. Carries both the domain-level
    listing result (storage paths and pagination token) and the unprocessed
    connector response for cases where connector-specific data is needed.

    Type Parameters:
        ConnectorResponseT: The type of the raw connector response.

    Attributes:
        storage_paths: Paths returned by the listing operation,
            inherited from ListResponse.
        continuation_token: Opaque pagination token for fetching the next page,
            inherited from ListResponse.
    """

    _: KW_ONLY
    raw_response: ConnectorResponseT
    """The unprocessed response returned directly by the connector."""
