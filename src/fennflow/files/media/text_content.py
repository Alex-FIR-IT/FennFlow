from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._sentinel import OMIT, Omittable, is_given
from fennflow.files.enums import MediaType

from .abstract.content import ContentPropertyAbstract
from .abstract.from_content import FromContentAbstract
from .base_binary import BaseBinary

if TYPE_CHECKING:
    from typing_extensions import Self

    from fennflow.files._annotations import MediaTypes


class TextContent(
    BaseBinary,
    FromContentAbstract,
    ContentPropertyAbstract,
):
    """Media content representing a plain text file.

    Stores text as UTF-8 encoded bytes internally.
    Use ``from_content()`` to create from a string.

    Attributes:
        encoding: The text encoding. Defaults to ``"utf-8"``.

    Example::

        file = TextContent.from_content("Hello, World!")
        print(file.content) # "Hello, World!"
        await uow.user_files.at("user1/").put(file)
    """

    encoding: str = "utf-8"

    @property
    def content(self) -> str:
        try:
            return self.data.decode(self.encoding)
        except UnicodeDecodeError as e:
            raise ValueError(f"Cannot extract text from {self=}") from e

    @classmethod
    def from_content(
        cls,
        data: str,
        media_type: MediaTypes = MediaType.TEXT_PLAIN,
        encoding: str = "utf-8",
        filename: Omittable[str] = OMIT,
        **kwargs,  # noqa: ARG003
    ) -> Self:
        extra = {}

        if is_given(filename):
            extra["filename"] = filename

        return cls(
            data=data.encode(encoding),
            media_type=media_type,
            encoding=encoding,
            **extra,
        )
