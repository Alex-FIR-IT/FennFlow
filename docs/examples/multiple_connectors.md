# Using Multiple Connectors

FennFlow makes it trivial to work with multiple object storages simultaneously. Each `UnitOfWork` owns
its own connector and backend scope, so you can compose them freely in the same coroutine.

## Example: Migrating files from AWS S3 to MinIO

```python
import asyncio

from fennflow import ConfigDict, UnitOfWork
from fennflow.backends import SqlalchemyBackendConfig
from fennflow.connectors import S3ConnectorConfig
from fennflow.repositories import (
    GetRepository,
    ListRepository,
    PutRepository,
    S3RepoField,
    )


class ReadRepository(GetRepository, ListRepository):
    pass


class WriteRepository(PutRepository):
    pass


class AWSS3UOW(UnitOfWork):
    files = S3RepoField(ReadRepository, bucket_name="my-bucket")
    config = ConfigDict(
        backend=SqlalchemyBackendConfig(scope="aws"),
        connector=S3ConnectorConfig(
            endpoint_url="https://s3.amazonaws.com",
            aws_access_key_id="aws-key",
            aws_secret_access_key="aws-secret",
            ),
        )


class MinIOUOW(UnitOfWork):
    files = S3RepoField(WriteRepository, bucket_name="my-bucket")
    config = ConfigDict(
        backend=SqlalchemyBackendConfig(scope="minio"),
        connector=S3ConnectorConfig(
            endpoint_url="https://minio.example.com",
            aws_access_key_id="minio-key",
            aws_secret_access_key="minio-secret",
            ),
        )


async def main():
    async with AWSS3UOW() as aws, MinIOUOW() as minio:
        paths = await aws.files.at("folder/").list()

        for path in paths:
            response = await aws.files.get(path)
            await minio.files.at("folder/").put(*response)


if __name__ == "__main__":
    asyncio.run(main())
```

The two UoWs are fully independent — different credentials, different endpoints, different backend scopes.
If anything fails mid-transfer, each UoW rolls back its own pending operations independently.