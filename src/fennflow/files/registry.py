from __future__ import annotations

from fennflow.files.enums import MediaType
from fennflow.files.media import (
    AudioContent,
    BinaryContent,
    DocumentContent,
    ImageContent,
    JsonContent,
    TextContent,
    VideoContent,
)

content_registry: dict[str, type[BinaryContent]] = {
    MediaType.TEXT_PLAIN: TextContent,
    "text/": TextContent,
    "image/": ImageContent,
    MediaType.APPLICATION_JSON: JsonContent,
    "audio/": AudioContent,
    "video/": VideoContent,
    MediaType.APPLICATION_OCTET_STREAM: DocumentContent,
}
