from __future__ import annotations

from fennflow.files.enums import MediaType
from fennflow.files.media import (
    AudioContent,
    BaseBinary,
    DocumentContent,
    ImageContent,
    JsonContent,
    TextContent,
    VideoContent,
)

content_registry: dict[str, type[BaseBinary]] = {
    MediaType.TEXT_PLAIN.value: TextContent,
    "text/": TextContent,
    "image/": ImageContent,
    MediaType.APPLICATION_JSON.value: JsonContent,
    "audio/": AudioContent,
    "video/": VideoContent,
    MediaType.APPLICATION_PDF.value: DocumentContent,
}
