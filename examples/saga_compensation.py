import asyncio

import httpx

from fennflow import ConfigDict, UnitOfWork
from fennflow.backends import SqlalchemyBackendConfig
from fennflow.connectors import S3ConnectorConfig
from fennflow.files import BinaryContent, ImageContent
from fennflow.repositories import (
    CreateRepository,
    GeneratePresignedUrlRepository,
    S3RepoField,
)


class AvatarRepository(CreateRepository, GeneratePresignedUrlRepository):
    pass


class AppUOW(UnitOfWork):
    avatars = S3RepoField(AvatarRepository, bucket_name="avatars")
    config = ConfigDict(
        backend=SqlalchemyBackendConfig(),
        connector=S3ConnectorConfig(
            endpoint_url="https://s3.amazonaws.com",
            aws_access_key_id="aws-key",
            aws_secret_access_key="aws-secret",
        ),
    )


async def process_avatar(user_id: str, avatar: ImageContent) -> None:
    async with AppUOW(auto_commit=False) as uow:
        await uow.avatars.at(user_id).create(avatar)

        presigned_url = await uow.avatars.generate_presigned_url(avatar.filename)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://verify.example.com/face",
                json={"url": presigned_url},
            )

        if response.status_code == 200:
            await uow.commit()
        # if verification failed or an exception was raised,
        # the UoW rolls back on exit — avatar is removed from S3 automatically


async def main():
    avatar = BinaryContent.from_local_path("avatar.jpg")
    await process_avatar(user_id="user-123", avatar=avatar)


if __name__ == "__main__":
    asyncio.run(main())
