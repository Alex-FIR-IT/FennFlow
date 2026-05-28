import asyncio
from dataclasses import dataclass

from fennflow import ConfigDict, UnitOfWork
from fennflow.backends import InMemoryBackendConfig
from fennflow.connectors import InMemoryConnectorConfig
from fennflow.repositories import GetRepository, S3RepoField


class AppUOW(UnitOfWork):
    avatars = S3RepoField(GetRepository, bucket_name="avatars")
    credentials = S3RepoField(GetRepository, bucket_name="credentials")

    config = ConfigDict(
        backend=InMemoryBackendConfig(),
        connector=InMemoryConnectorConfig(),
    )


@dataclass(slots=True)
class AvatarPath:
    user_id: int

    def render(self) -> str:
        return f"avatars/user_{self.user_id}"


@dataclass(slots=True)
class PassportPath:
    user_id: int

    def render(self) -> str:
        return f"credentials/user_{self.user_id}/passport"


@dataclass(slots=True)
class DriverLicensePath:
    user_id: int

    def render(self) -> str:
        return f"credentials/user_{self.user_id}/driver_license"


async def main():
    user_id = 535

    async with AppUOW() as uow:
        avatar_storage = uow.avatars.at(AvatarPath(user_id=user_id))
        assert avatar_storage.cwd == "avatars/user_535/"

        passport_storage = uow.credentials.at(PassportPath(user_id=user_id))
        assert passport_storage.cwd == "credentials/user_535/passport/"

        driver_license_storage = uow.credentials.at(DriverLicensePath(user_id=user_id))
        assert driver_license_storage.cwd == "credentials/user_535/driver_license/"


if __name__ == "__main__":
    asyncio.run(main())
