from __future__ import annotations

import json
from typing import TYPE_CHECKING

from fennflow._sentinel import OMIT, Omittable, is_given
from fennflow.files.enums import MediaType

from .abstract.content import ContentPropertyAbstract
from .abstract.from_content import FromContentAbstract
from .base_binary import BaseBinary

if TYPE_CHECKING:
    from pydantic import JsonValue

    from fennflow.files._annotations import MediaTypes


class JsonContent(
    BaseBinary,
    FromContentAbstract,
    ContentPropertyAbstract,
):
    """Media content representing a JSON file.

    Stores JSON data as UTF-8 encoded bytes internally.
    Use ``from_content()`` to create from a Python object.

    Attributes:
        encoding: The text encoding. Defaults to ``"utf-8"``.

    Example::

        file = JsonContent.from_content({"key": "value"})
        print(file.content) # {"key": "value"}
        await uow.user_files.at("user1/").put(file)
    """

    encoding: str = "utf-8"

    @property
    def content(self) -> JsonValue:
        text = self.data.decode(self.encoding)
        return json.loads(text)

    @classmethod
    def from_content(
        cls,
        data: JsonValue,
        media_type: MediaTypes = MediaType.APPLICATION_JSON,
        encoding: str = "utf-8",
        filename: Omittable[str] = OMIT,
        ensure_ascii: bool = False,
        indent: int | str | None = None,
        **extra_json_dumps_kwargs,
    ) -> JsonContent:
        dumped_data = json.dumps(
            data,
            ensure_ascii=ensure_ascii,
            indent=indent,
            **extra_json_dumps_kwargs,
        )

        extra = {}
        if is_given(filename):
            extra["filename"] = filename

        return cls(
            data=dumped_data.encode(encoding),
            media_type=media_type,
            encoding=encoding,
            **extra,
        )
