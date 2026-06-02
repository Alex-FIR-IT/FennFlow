from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import pytest

from fennflow.files import TextContent

if TYPE_CHECKING:
    from tests.shared.uows import MinioUOW


@pytest.mark.asyncio
async def test_generate_presigned_url_returns_content(uow_cls: type[MinioUOW]):
    text = "test_generate_presigned_url_returns_content"

    file = TextContent.from_content(text)
    async with uow_cls() as uow:
        await uow.user_files.create(file)

        response = await uow.user_files.generate_presigned_url(
            file.filename,
            "NonExistentFilename",
        )
        urls = tuple(response.urls)

        assert isinstance(response.results, list)
        assert len(response.results) == 2
        assert len(urls) == 1

        async with httpx.AsyncClient() as client:
            presigned_url_response = await client.get(*urls)

            assert presigned_url_response.content == file.data
