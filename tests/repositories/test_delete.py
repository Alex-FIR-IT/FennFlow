import pytest


@pytest.mark.asyncio
async def test_delete_removes_file(uow_cls, text_files):
    async with uow_cls() as uow:
        await uow.user_files.at("user/").create(*text_files)

        await uow.user_files.at("user/").delete(text_files[0].filename)

        result = await uow.user_files.at("user/").get(text_files[0].filename)
        assert len(result) == 0

        result = await uow.user_files.at("user/").get(text_files[1].filename)
        assert len(result) == 1


@pytest.mark.asyncio
async def test_delete_after_commit(uow_cls, text_files):
    async with uow_cls() as uow:
        await uow.user_files.at("user/").create(*text_files)
        await uow.commit()
        await uow.user_files.at("user/").delete(text_files[0].filename)

        result = await uow.user_files.at("user/").get(text_files[0].filename)
        assert len(result) == 0
        await uow.commit()
        result = await uow.user_files.at("user/").get(text_files[0].filename)
        assert len(result) == 0


@pytest.mark.asyncio
async def test_delete_several_times_and_rollback(uow_cls, text_files):
    file = text_files[0]
    async with uow_cls() as uow:
        response = await uow.user_files.create(file)
        await uow.commit()

        for _ in range(100):
            await uow.user_files.delete(file.filename)

        response = await uow.user_files.get(file.filename)
        assert len(response) == 0

        await uow.rollback()

        response = await uow.user_files.get(file.filename)
        assert len(response) == 1
        assert response[0].content.data == file.data
