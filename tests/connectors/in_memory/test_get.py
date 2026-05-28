import pytest

from fennflow.connectors import InMemoryConnector


@pytest.mark.asyncio
async def test_not_calling_connector_for_not_uploaded(
    uow_cls,
    text_files,
    monkeypatch,
):
    get_count = 0
    original_get = InMemoryConnector.get

    async def count_get(*args, **kwargs):
        nonlocal get_count

        get_count += 1
        return await original_get(*args, **kwargs)

    monkeypatch.setattr(InMemoryConnector, "get", count_get)

    async with uow_cls() as uow:
        response = await uow.user_files.get(text_files[0].filename)
        assert len(response) == 0
        assert get_count == 0

        await uow.user_files.create(*text_files)

        response = await uow.user_files.get(text_files[0].filename)

        assert len(response) == 1
        assert get_count == 1

        await uow.commit()

        response = await uow.user_files.get(text_files[0].filename)

        assert len(response) == 1
        assert get_count == 2

        response = await uow.user_files.delete(text_files[0].filename)

        response = await uow.user_files.get(text_files[0].filename)

        assert len(response) == 0
        assert get_count == 2

        await uow.rollback()

        response = await uow.user_files.get(text_files[0].filename)

        assert len(response) == 1
        assert get_count == 3

        response = await uow.user_files.get(text_files[1].storage_path)

        assert len(response) == 1
        assert get_count == 4
