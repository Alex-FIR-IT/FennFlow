from typing import TypeAlias

from . import BinaryContent
from .media import (
    AudioContent,
    BaseBinary,
    DocumentContent,
    ImageContent,
    JsonContent,
    TextContent,
    UrlContent,
    VideoContent,
)

VideoOrAudio: TypeAlias = VideoContent | AudioContent

BinaryMedia: TypeAlias = (
    JsonContent
    | VideoContent
    | DocumentContent
    | ImageContent
    | AudioContent
    | TextContent
    | BaseBinary
    | BinaryContent
)

Media: TypeAlias = BinaryMedia | UrlContent
