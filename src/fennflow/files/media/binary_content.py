from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from fennflow._sentinel import OMIT, Omittable, is_given
from fennflow.files._media_type_guesser import MimeTypeGuesser

from .base_binary import BaseBinary

if TYPE_CHECKING:
    from typing_extensions import Self

    from fennflow.files._annotations import MediaTypes


class BinaryContent(BaseBinary):
    """Class for arbitrary binary data."""

    @classmethod
    def from_local_path(
        cls,
        path: str | Path,
        media_type: Omittable[MediaTypes] = OMIT,
        **kwargs: Any,
    ) -> Self:
        """Create a ``BinaryContent`` instance from the local filesystem.

        The MIME type is guessed from the file extension when ``media_type`` is not
        provided. The filename is taken from the final component of ``path`` and can
        be overridden via ``kwargs``.

        Unlike ``ContentFactory.from_local_path``, this method always returns an
        instance of the class it is called on — it never resolves a richer subtype
        from the content registry.

        Args:
            path: Absolute or relative path to the file, as a ``str`` or
                ``pathlib.Path``.
            media_type: MIME type to assign to the content. When omitted, the type
                is guessed from the file extension via ``MimeTypeGuesser``.
            **kwargs: Additional fields forwarded to the content model (e.g.
                ``filename`` to override the name derived from ``path``,
                or arbitrary keys stored in ``extra_metadata``).

        Returns:
            An instance of ``BinaryContent`` (or the subclass this method is called
            on) containing the file's raw bytes and resolved metadata.

        Raises:
            FileNotFoundError: If ``path`` does not point to an existing file.
            ExtensionCannotBeGuessed: If ``media_type`` is omitted and the extension
                cannot be mapped to a known MIME type.

        Example::

            from fennflow.files import MediaType
            from fennflow.files import BinaryContent

            # MIME type guessed from extension
            content = BinaryContent.from_local_path("report.pdf")

            # Explicit MIME type
            content = BinaryContent.from_local_path(
                "dump.bin",
                media_type=MediaType.APPLICATION_OCTET_STREAM,
            )

            # Override filename and attach extra metadata
            content = BinaryContent.from_local_path(
                "/tmp/upload_xyz",
                media_type=MediaType.IMAGE_PNG,
                filename="avatar.png",
                uploaded_by="alice",
            )


        Notes:
            This method is not inherited by other binary content classes
            such as TextContent, ImageContent, etc. Because this method returns
            an instance of the class it is called on, inheritance would allow
            incorrect usage — for example, obtaining an ImageContent instance
            from "text.txt". To get a specific content type, use
            ContentFactory.from_local_path or the class constructor directly
            (e.g. ImageContent(...)).
        """
        filename = Path(path).name

        if not is_given(media_type):
            media_type = MimeTypeGuesser.guess_type(filename=filename)

        kwargs.setdefault("filename", filename)

        with open(path, "rb") as file:
            return cls(
                media_type=media_type,
                data=file.read(),
                **kwargs,
            )
