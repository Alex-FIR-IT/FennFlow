from __future__ import annotations

import mimetypes
from typing import TYPE_CHECKING

from fennflow._extra_mimetypes import EXTENSION_TO_CONTENT_TYPE
from fennflow._sentinel import OMIT, Omittable, is_given
from fennflow.files.exceptions import (
    ExtensionCannotBeGuessed,
    MediaTypeCannotBeGuessedException,
)

if TYPE_CHECKING:
    from fennflow.files._annotations import MediaTypes


for ext, mimetype in EXTENSION_TO_CONTENT_TYPE.items():
    mimetypes.add_type(mimetype, f".{ext}")


class MimeTypeGuesser:
    @staticmethod
    def guess_type(
        filename: str,
        strict: bool = False,
        fallback_media_type: Omittable[MediaTypes] = OMIT,
    ) -> str:
        original_filename = filename
        if not filename.split(".")[0]:
            # mimetypes.guess_type fails on dotfiles (e.g. ".env")
            # — prepend a stem to fix it
            filename = f"stem{filename}"

        guessed_media_type = mimetypes.guess_type(
            filename,
            strict=strict,
        )[0]

        if guessed_media_type is None:
            if is_given(fallback_media_type):
                return fallback_media_type
            raise MediaTypeCannotBeGuessedException(filename=original_filename)

        return guessed_media_type

    @staticmethod
    def guess_extension(
        media_type: MediaTypes,
        strict: bool = False,
        return_exception: bool = False,
    ) -> str | ExtensionCannotBeGuessed:
        guessed_extension = mimetypes.guess_extension(
            media_type,
            strict=strict,
        )

        if guessed_extension is None:
            exception = ExtensionCannotBeGuessed(
                f"Cannot guess extension for {media_type=}. "
            )
            if return_exception:
                return exception
            raise exception

        return guessed_extension
