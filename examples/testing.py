import pytest
import pytest_asyncio

from fennflow import ConfigDict, UnitOfWork
from fennflow.backends import InMemoryBackendConfig, SqlalchemyBackendConfig
from fennflow.connectors import InMemoryConnectorConfig, S3ConnectorConfig
from fennflow.files import ImageContent
from fennflow.repositories import CreateRepository, GetRepository, S3RepoField


class AvatarRepository(CreateRepository, GetRepository):
    pass


class AppUOW(UnitOfWork):
    avatars = S3RepoField(AvatarRepository, bucket_name="avatars")
    config = ConfigDict(
        backend=SqlalchemyBackendConfig(),
        connector=S3ConnectorConfig(),
    )


class TestUOW(AppUOW):
    config = ConfigDict(
        backend=InMemoryBackendConfig(),
        connector=InMemoryConnectorConfig(),
    )


class DbClient:
    async def create_user(self, user_id: str, avatar_path: str) -> None: ...


async def register_user(
    user_id: str,
    avatar: ImageContent,
    uow: AppUOW,
    db: DbClient,
) -> None:
    async with uow:
        await uow.avatars.at(user_id).create(avatar)
        await db.create_user(user_id=user_id, avatar_path=avatar.filename)


@pytest_asyncio.fixture
def db():
    return DbClient()


@pytest.mark.asyncio
async def test_register_user_saves_avatar(db):
    avatar = ImageContent(
        data=b"fake-image-bytes",
        media_type="image/jpeg",
        filename="avatar.jpg",
    )

    await register_user(user_id="user-123", avatar=avatar, uow=TestUOW(), db=db)

    async with TestUOW() as uow:
        response = await uow.avatars.at("user-123").get("avatar.jpg")
        assert response.images[0].filename == "avatar.jpg"
