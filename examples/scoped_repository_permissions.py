import asyncio

from fennflow import ConfigDict, UnitOfWork
from fennflow.backends import SqlalchemyBackendConfig
from fennflow.connectors import S3ConnectorConfig
from fennflow.files import BinaryContent
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
    report_file = BinaryContent.from_local_path("report.txt")

    async with AppUOW() as uow:
        # Full access on main storage
        await uow.files.at("reports/").put(report_file)
        await uow.files.delete("reports/old_report.pdf")

        # Safe write on backup — create raises if file already exists,
        # delete and overwrite are simply not available
        await uow.backups.at("reports/").create(report_file)


if __name__ == "__main__":
    asyncio.run(main())
