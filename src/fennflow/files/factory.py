from __future__ import annotations

from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import ValidationError

from fennflow._sentinel import OMIT, Omittable, is_given
from fennflow.files._filename_generator import FilenameGenerator
from fennflow.files._media_type_guesser import MimeTypeGuesser
from fennflow.files.enums import MediaType
from fennflow.files.media.base_binary import BaseBinary
from fennflow.files.media.url_content import UrlContent
from fennflow.files.registry import content_registry

if TYPE_CHECKING:
    from fennflow.files._annotations import MediaTypes
    from fennflow.files.types import BinaryMedia


class ContentFactory:
    """Factory for creating media content instances from raw data.

    Resolves the appropriate content class from the registry based on
    MIME type, falling back to ``BaseBinary`` for unknown types.

    """

    @staticmethod
    @cache
    def _get_prefixes() -> list[str]:
        """Return registry prefixes sorted by length descending for match resolution."""
        return sorted(
            (p for p in content_registry if p.endswith("/")),
            key=len,
            reverse=True,
        )

    @classmethod
    def from_bytes(
        cls,
        media_type: MediaTypes,
        data: bytes,
        **kwargs: Any,
    ) -> BinaryMedia:
        """Create a media content instance from raw bytes.

        Resolves the content class from the registry by exact MIME type match,
        then by prefix match, falling back to ``BaseBinary`` if no match is found.

        Args:
            media_type: The MIME type of the content (e.g. ``"text/plain"``).
            data: The raw bytes to wrap.
            **kwargs: Additional fields passed to the content model.

        Returns:
            A media content instance appropriate for the given MIME type.

        Raises:
            ValueError: If the resolved content class fails validation.

        **Example**:

            from fennflow.files import MediaType
            content = ContentFactory.from_bytes(MediaType.TEXT_PLAIN, b"Hello, World!")
        """
        payload = {
            "media_type": media_type,
            "data": data,
            **kwargs,
        }

        if media_type in content_registry:
            content_cls = content_registry[media_type]
        else:
            for prefix in cls._get_prefixes():
                if media_type.startswith(prefix):
                    content_cls = content_registry[prefix]
                    break
            else:
                content_cls = BaseBinary

        try:
            return content_cls.model_validate(payload)
        except ValidationError as exc:
            raise ValueError(
                f"Failed to validate {content_cls.__name__=} for {media_type=}"
            ) from exc

    @staticmethod
    def from_url(
        url: str,
        media_type: MediaTypes = MediaType.APPLICATION_OCTET_STREAM,
        **kwargs: Any,
    ) -> UrlContent:
        """Create a ``UrlContent`` instance from a URL string.

        Args:
            url: The URL string to wrap.
            media_type: The MIME type of the resource.
                Defaults to ``"application/octet-stream"``.
            **kwargs: Additional fields passed to the content model.

        Returns:
            A ``UrlContent`` instance wrapping the given URL.

        Raises:
            ValueError: If the resolved content class fails validation.

        **Example**::

            url = ContentFactory.from_url("https://example.com/file.txt")
        """
        if "filename" not in kwargs:
            kwargs["filename"] = FilenameGenerator.generate_from_url(url)

        payload = {
            "data": url,
            "media_type": media_type,
            **kwargs,
        }

        try:
            return UrlContent.model_validate(payload)
        except ValidationError as exc:
            raise ValueError(f"Failed to create UrlContent for {url=}") from exc

    @classmethod
    def from_local_path(
        cls,
        path: str | Path,
        media_type: Omittable[MediaTypes] = OMIT,
        **kwargs: Any,
    ) -> BinaryMedia:
        filename = Path(path).name

        if not is_given(media_type):
            media_type = MimeTypeGuesser.guess_type(filename=filename)

        kwargs.setdefault("filename", filename)

        with open(path, "rb") as file:
            return cls.from_bytes(
                data=file.read(),
                media_type=media_type,
                **kwargs,
            )
