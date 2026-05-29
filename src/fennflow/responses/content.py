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
    # covariant=True,
)


@dataclass(slots=True)
class ContentResponse(  # noqa: D101
    ConnectorRawResponse[ConnectorResponseT],
    Generic[ConnectorResponseT, ContentResponseT],
):
    content: ContentResponseT
