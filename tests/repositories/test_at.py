import pytest

from tests.shared.path_templates import (
    MonthPath,
    MonthPathWithTrailingSlash,
    UserPath,
    UserPathWithTrailingSlash,
)


@pytest.mark.asyncio
async def test_chain_at(uow_cls):
    async with uow_cls() as uow:
        storage = uow.user_files.at("user/")
        assert storage.cwd == "user/"
        storage = storage.at("shelf1/")
        assert storage.cwd == "user/shelf1/"
        storage = storage.at("/")
        assert storage.cwd == "user/shelf1/"


@pytest.mark.asyncio
async def test_many_slashes_at(uow_cls):
    async with uow_cls() as uow:
        storage = uow.user_files.at("user//////")
        assert storage.cwd == "user/"


@pytest.mark.asyncio
async def test_root_folder_at(uow_cls):
    async with uow_cls() as uow:
        storage = uow.user_files.at("/")
        assert storage.cwd == ""
        storage = storage.at("/user1/")
        assert storage.cwd == "user1/"


@pytest.mark.asyncio
async def test_empty_path(uow_cls):
    async with uow_cls() as uow:
        storage = uow.user_files.at("")
        assert storage.cwd == ""


@pytest.mark.asyncio
async def test_complex_path_normalization(uow_cls):
    async with uow_cls() as uow:
        storage = uow.user_files.at("///user///shelf1///")
        assert storage.cwd == "user/shelf1/"


@pytest.mark.asyncio
async def test_chained_normalization(uow_cls):
    async with uow_cls() as uow:
        storage = uow.user_files.at("///user///")
        storage = storage.at("///shelf1///")
        assert storage.cwd == "user/shelf1/"


@pytest.mark.asyncio
async def test_storages_isolation(uow_cls):
    async with uow_cls() as uow:
        storage1 = uow.user_files.at("user/")
        storage2 = uow.user_files.at("admin/")
        assert storage1.cwd == "user/"
        assert storage2.cwd == "admin/"


@pytest.mark.asyncio
async def test_default_cwd(uow_cls):
    async with uow_cls() as uow:
        assert uow.user_files.cwd == ""


class TestPathTemplates:
    @pytest.mark.asyncio
    @staticmethod
    async def test_at_resolves_path_template(uow_cls):
        """at() should resolve a PathTemplate to its rendered string path."""
        async with uow_cls() as uow:
            scoped = uow.user_files.at(UserPath(user_id=42))
            assert scoped.cwd == "users/user_42/"

    @pytest.mark.asyncio
    @staticmethod
    async def test_at_raises_type_error_for_invalid_input(uow_cls):
        """at() should raise TypeError.

        When passed something other than str or PathTemplate.
        """
        async with uow_cls() as uow:
            with pytest.raises(TypeError, match="at()"):
                uow.user_files.at(123)  # type: ignore[arg-type]

    @pytest.mark.asyncio
    @staticmethod
    async def test_at_raises_type_error_message_is_actionable(uow_cls):
        """TypeError message should mention render() so the user knows how to fix it."""
        async with uow_cls() as uow:
            with pytest.raises(TypeError, match="render()"):
                uow.user_files.at(object())  # type: ignore[arg-type]

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "first, second, expected",
        [
            # str + str
            ("users/user_1", "2025/06", "users/user_1/2025/06/"),
            ("users/user_1/", "2025/06", "users/user_1/2025/06/"),
            ("users/user_1", "2025/06/", "users/user_1/2025/06/"),
            ("users/user_1/", "2025/06/", "users/user_1/2025/06/"),
            # template + str
            (UserPath(user_id=1), "2025/06", "users/user_1/2025/06/"),
            (UserPathWithTrailingSlash(user_id=1), "2025/06", "users/user_1/2025/06/"),
            (UserPath(user_id=1), "2025/06/", "users/user_1/2025/06/"),
            # str + template
            ("users/user_1", MonthPath(year=2025, month=6), "users/user_1/2025/06/"),
            ("users/user_1/", MonthPath(year=2025, month=6), "users/user_1/2025/06/"),
            (
                "users/user_1",
                MonthPathWithTrailingSlash(year=2025, month=6),
                "users/user_1/2025/06/",
            ),
            # template + template
            (
                UserPath(user_id=1),
                MonthPath(year=2025, month=6),
                "users/user_1/2025/06/",
            ),
            (
                UserPathWithTrailingSlash(user_id=1),
                MonthPath(year=2025, month=6),
                "users/user_1/2025/06/",
            ),
            (
                UserPath(user_id=1),
                MonthPathWithTrailingSlash(year=2025, month=6),
                "users/user_1/2025/06/",
            ),
            (
                UserPathWithTrailingSlash(user_id=1),
                MonthPathWithTrailingSlash(year=2025, month=6),
                "users/user_1/2025/06/",
            ),
        ],
    )
    @staticmethod
    async def test_at_chain_normalizes_slashes(first, second, expected, uow_cls):
        """Chained at() calls should produce a correctly normalized path regardless
        of whether strings or templates include trailing slashes."""
        async with uow_cls() as uow:
            scoped = uow.user_files.at(first).at(second)
            assert scoped.cwd == expected
