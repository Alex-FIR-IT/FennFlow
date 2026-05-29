import pytest


@pytest.mark.asyncio
async def test_get_returns_empty_response_for_non_existing_file(uow_cls):

    async with uow_cls() as uow:
        response = await uow.connector.get(
            storage_path="fdf",
            repo_extra=uow.files.repo_extra,
        )
        assert len(response) == 0
