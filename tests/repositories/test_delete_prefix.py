import pytest

from fennflow.files import TextContent


@pytest.mark.asyncio
async def test_delete_prefix_removes_all_files(uow_cls, text_files):
    async with uow_cls() as uow:
        await uow.user_files.at("user/").create(*text_files)

        await uow.user_files.at("user/").delete_prefix("")

        for file in text_files:
            result = await uow.user_files.at("user/").get(file.filename)
            assert len(result) == 0


@pytest.mark.asyncio
async def test_delete_prefix_removes_only_matched_files(uow_cls, text_files):
    async with uow_cls() as uow:
        await uow.user_files.at("user1/").create(text_files[0])
        await uow.user_files.at("user2/").create(text_files[1])

        await uow.user_files.delete_prefix("user1/")

        result = await uow.user_files.at("user1/").get(text_files[0].filename)
        assert len(result) == 0

        result = await uow.user_files.at("user2/").get(text_files[1].filename)
        assert len(result) == 1


@pytest.mark.asyncio
async def test_delete_prefix_empty_prefix_removes_all(uow_cls, text_files):
    async with uow_cls() as uow:
        await uow.user_files.at("user1/").create(text_files[0])
        await uow.user_files.at("user2/").create(text_files[1])

        await uow.user_files.delete_prefix("")

        for file in text_files:
            result = await uow.user_files.get(file.filename)
            assert len(result) == 0


@pytest.mark.asyncio
async def test_delete_prefix_no_matches_returns_empty(uow_cls, text_files):
    async with uow_cls() as uow:
        await uow.user_files.at("user/").create(*text_files)

        results = await uow.user_files.delete_prefix("nonexistent/")

        assert results == []


@pytest.mark.asyncio
async def test_delete_prefix_rollback(uow_cls, text_files):
    async with uow_cls() as uow:
        await uow.user_files.at("user/").create(*text_files)
        await uow.commit()

        await uow.user_files.delete_prefix("user/")

        for file in text_files:
            result = await uow.user_files.at("user/").get(file.filename)
            assert len(result) == 0

        await uow.rollback()

        for file in text_files:
            result = await uow.user_files.at("user/").get(file.filename)
            assert len(result) == 1


@pytest.mark.asyncio
async def test_delete_prefix_after_commit(uow_cls, text_files):
    async with uow_cls() as uow:
        await uow.user_files.at("user/").create(*text_files)
        await uow.commit()

        await uow.user_files.delete_prefix("user/")
        await uow.commit()

        for file in text_files:
            result = await uow.user_files.at("user/").get(file.filename)
            assert len(result) == 0


@pytest.mark.asyncio
async def test_delete_prefix_pagination(uow_cls):
    files = [TextContent.from_content(f"file{i}") for i in range(1050)]
    async with uow_cls() as uow:
        await uow.user_files.at("bulk/").create(*files)
        await uow.commit()

        response = await uow.user_files.delete_prefix("bulk/")
        assert len(response) == 1050
        assert all(response) is True
        await uow.commit()

        results = await uow.user_files.at("bulk/").list()
        assert len(results) == 0
