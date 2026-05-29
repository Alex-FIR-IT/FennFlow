from __future__ import annotations

from dataclasses import dataclass
from typing import Generic

from typing_extensions import TypeVar

from fennflow.files.types import Media
from fennflow.responses.connector_raw import ConnectorRawResponse

ConnectorResponseT = TypeVar("ConnectorResponseT")
ContentResponseT = TypeVar(
    "ContentResponseT",
    bound=Media,
)


@dataclass(slots=True)
class ContentResponse(
    ConnectorRawResponse[ConnectorResponseT],
    Generic[ConnectorResponseT, ContentResponseT],
):
    """Wraps a media content object alongside the raw connector response.

    Returned by connector read operations that produce a single media item.
    Preserves the raw connector response for advanced use cases such as
    accessing connector-specific metadata not captured in the domain model.

    Type Parameters:
        ConnectorResponseT: The type of the raw connector response.
        ContentResponseT: The type of the resolved media content,
            bound to Media.

    """

    content: ContentResponseT
    """The resolved media content instance."""
