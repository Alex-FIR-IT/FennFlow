# Working with File Content

FennFlow wraps raw bytes in typed content models. Instead of juggling `bytes` and `dict`,
you work with `TextContent`, `JsonContent`, `BinaryContent` and others — each with typed accessors
for their data.

## Example: Creating, uploading and retrieving typed files

```python
import asyncio

from fennflow import ConfigDict, UnitOfWork
from fennflow.backends import SqlalchemyBackendConfig
from fennflow.connectors import S3ConnectorConfig
from fennflow.files import BinaryContent, JsonContent, MediaType, TextContent
from fennflow.repositories import (
    CreateRepository,
    GetRepository,
    ListRepository,
    S3RepoField,
    )


class ReadWriteRepository(CreateRepository, GetRepository, ListRepository):
    pass


class AppUOW(UnitOfWork):
    files = S3RepoField(ReadWriteRepository, bucket_name="my-bucket")
    config = ConfigDict(
        backend=SqlalchemyBackendConfig(),
        connector=S3ConnectorConfig(
            endpoint_url="https://s3.amazonaws.com",
            aws_access_key_id="aws-key",
            aws_secret_access_key="aws-secret",
            ),
        )


async def main():
    # Three ways to create file content
    text_file = TextContent.from_content("Hello, world!")
    json_file = JsonContent.from_content({"user": "alice", "score": 42})

    from_local_path_binary = BinaryContent.from_local_path("my_file.txt")
    binary_file = BinaryContent(data=b"some bytes", media_type=MediaType.APPLICATION_OCTET_STREAM)

    async with AppUOW() as uow:
        await uow.files.at("folder/").create(text_file, json_file, binary_file)

        paths = await uow.files.at("folder/").list()
        response = await uow.files.get(*paths)

        print(response.texts[0].content)  # "Hello, world!"
        print(response.texts[1].filename)  # "my_file.txt"

        print(response.filter(JsonContent)[0].content)  # {"user": "alice", "score": 42}
        print(response.filter_by_media_type(MediaType.APPLICATION_OCTET_STREAM)[0].data)  # b"some bytes"


if __name__ == "__main__":
    asyncio.run(main())
```

`TextContent.content` returns a `str`, `JsonContent.content` returns the parsed Python object —
no manual `decode()` or `json.loads()` needed.

MediaResponse uses `ContentFactory` to resolve the correct class on retrieval
automatically based on the stored MIME type, so `.texts`, `.filter()`, `.filter_by_media_type()` and other
typed accessors on `MediaResponse` always return the right types.
