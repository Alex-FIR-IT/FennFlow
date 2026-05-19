from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from fennflow._operations.context.abstract import BaseContext
from fennflow.files import TextContent

if TYPE_CHECKING:
    from fennflow.backends import InMemoryBackend


@pytest.mark.asyncio
async def test_operation_context_is_cleared_with_commit(uow_cls):
    async with uow_cls() as uow:
        for i in range(5):
            await uow.user_files.at("folder1/").create(
                TextContent.from_content(f"file{i}")
            )

        await uow.commit()

        assert len(uow.backend.session_buffer.get_all()) == 0

        backend: InMemoryBackend = uow.backend.backend_engine

        for operation in backend.scoped_storage.values():
            assert type(operation.context) is BaseContext


@pytest.mark.asyncio
async def test_operation_context_is_cleared_in_new_session(uow_cls):
    async with uow_cls() as uow:
        for i in range(5):
            await uow.user_files.at("folder1/").create(
                TextContent.from_content(f"file{i}")
            )

    async with uow_cls() as uow:
        assert len(uow.backend.session_buffer.get_all()) == 0

        backend: InMemoryBackend = uow.backend.backend_engine

        for operation in backend.scoped_storage.values():
            assert type(operation.context) is BaseContext
