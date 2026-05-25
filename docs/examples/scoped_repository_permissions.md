# Scoped Repository Permissions

FennFlow's mixin architecture lets each repository expose only the operations it should allow.
Instead of a single god-repository with full access everywhere, you compose exactly the capabilities
each part of your system needs — nothing more.

## Example: Main storage with full access, backup storage with safe write-only access

```python
import asyncio

from fennflow import ConfigDict, UnitOfWork
from fennflow.backends import SqlalchemyBackendConfig
from fennflow.connectors import S3ConnectorConfig
from fennflow.files import ContentFactory, MediaType
from fennflow.repositories import (
    CreateRepository,
    DeleteRepository,
    GetRepository,
    PutRepository,
    S3RepoField,
    )


class CRUDRepository(
    CreateRepository,
    DeleteRepository,
    GetRepository,
    PutRepository,
    ):
    pass


class SafeWriteReadRepository(
    CreateRepository,
    GetRepository,
    ):
    pass


class AppUOW(UnitOfWork):
    files = S3RepoField(CRUDRepository, bucket_name="main-bucket")
    backups = S3RepoField(SafeWriteReadRepository, bucket_name="backup-bucket")
    config = ConfigDict(
        backend=SqlalchemyBackendConfig(),
        connector=S3ConnectorConfig(
            endpoint_url="https://s3.amazonaws.com",
            aws_access_key_id="aws-key",
            aws_secret_access_key="aws-secret",
            ),
        )


async def main():
    with open("report.txt", "rb") as file:
        report_file = ContentFactory.from_bytes(
            data=file.read(),
            media_type=MediaType.TEXT_PLAIN,
            )
    async with AppUOW() as uow:
        # Full access on main storage
        await uow.files.at("reports/").put(report_file)
        await uow.files.delete("reports/old_report.pdf")

        # Safe write on backup — create raises if file already exists,
        # delete and overwrite are simply not available
        await uow.backups.at("reports/").create(report_file)


if __name__ == "__main__":
    asyncio.run(main())

```

`SafeWriteReadRepository` has no `put` and no `delete` — not restricted at runtime, just never composed in.
Misuse is a `AttributeError` at development time, not a bug in production.