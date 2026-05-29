import pytest


@pytest.mark.asyncio
async def test_file_recovery_after_deleting_on_rollback(
    uow_cls,
    text_files,
    scope,
    namespace,
):
    async with uow_cls() as uow:
        await uow.user_files.at("user/").create(text_files[0])

    async with uow_cls(auto_commit=False) as uow:
        get_response = await uow.user_files.at("user/").get(text_files[0].filename)
        assert len(get_response) == 1, f"Expected 1 file, got {len(get_response)}"
        assert get_response[0].content.data == text_files[0].data

        await uow.user_files.at("user/").delete(text_files[0].filename)

        response = await uow.user_files.at("user/").get(text_files[0].filename)
        assert len(response) == 0

    async with uow_cls() as uow:
        response = await uow.user_files.at("user/").get(text_files[0].filename)
        assert len(response) == 1, f"Expected 1 file, got {len(response)}"
        assert response[0].content.data == text_files[0].data

        operation = await uow.backend.get(
            storage_path=text_files[0].storage_path,
            scope=scope,
            namespace=namespace,
        )

        assert operation.record.is_uploaded is True
