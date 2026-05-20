from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from fennflow._operations.context.abstract import BaseContext
from fennflow._operations.dto import Record
from fennflow.files import TextContent

if TYPE_CHECKING:
    from fennflow.backends import InMemoryBackend


@pytest.mark.asyncio
async def test_record_without_context_in_backend(uow_cls):
    async with uow_cls() as uow:
        for i in range(5):
            await uow.user_files.at("folder1/").create(
                TextContent.from_content(f"file{i}")
            )

        await uow.commit()

        assert len(uow.backend.session_buffer.get_all()) == 0

        backend: InMemoryBackend = uow.backend.backend_engine

        for record in backend.scoped_storage.values():
            assert isinstance(record, Record) is True
            assert getattr(record, "context", None) is None
