from __future__ import annotations

import pytest

from fennflow.files import TextContent


@pytest.mark.asyncio
async def test_session_buffer_empty_after_commit(uow_cls):
    async with uow_cls() as uow:
        for i in range(5):
            await uow.user_files.at("folder1/").create(
                TextContent.from_content(f"file{i}")
            )

        await uow.commit()

        assert len(uow.backend.session_buffer.get_all()) == 0


@pytest.mark.asyncio
async def test_session_buffer_empty_after_rollback(uow_cls):
    async with uow_cls() as uow:
        for i in range(5):
            await uow.user_files.at("folder1/").create(
                TextContent.from_content(f"file{i}")
            )

        await uow.rollback()

        assert len(uow.backend.session_buffer.get_all()) == 0


@pytest.mark.asyncio
async def test_session_buffer_empty_after_aexit(uow_cls):
    async with uow_cls() as uow:
        for i in range(5):
            await uow.user_files.at("folder1/").create(
                TextContent.from_content(f"file{i}")
            )

    assert len(uow.backend.session_buffer.get_all()) == 0
