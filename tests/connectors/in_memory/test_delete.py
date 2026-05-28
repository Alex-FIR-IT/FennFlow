import pytest

from fennflow.connectors import InMemoryConnector


@pytest.mark.asyncio
async def test_delete_not_calling_connector_for_status_deleted(
    uow_cls,
    text_files,
    monkeypatch,
):
    delete_count = 0
    original_delete = InMemoryConnector.delete

    async def tracking_delete(self, storage_path, repo_extra, **extra):
        nonlocal delete_count
        delete_count += 1
        await original_delete(self, storage_path, repo_extra, **extra)

    monkeypatch.setattr(InMemoryConnector, "delete", tracking_delete)

    async with uow_cls() as uow:
        await uow.user_files.at("user/").create(*text_files)
        await uow.user_files.at("user/").delete(text_files[0].filename)
        assert delete_count == 1
        await uow.user_files.at("user/").delete(text_files[0].filename)
        assert delete_count == 1

        await uow.commit()
        assert (
            delete_count == 2
        )  # compensation deleted a tmp file, thus delete_count is incremented
        await uow.user_files.at("user/").delete(text_files[0].filename)
        assert delete_count == 2
