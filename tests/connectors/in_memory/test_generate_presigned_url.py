from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from fennflow.connectors.exceptions import ConnectorCapabilityException

if TYPE_CHECKING:
    from tests.shared.uows import TestUOW


@pytest.mark.asyncio
async def test_generate_presigned_url_raises_capability_error(uow_cls, text_files):
    async with uow_cls() as uow:
        await uow.user_files.create(text_files[0])

        with pytest.raises(ConnectorCapabilityException):
            await uow.user_files.generate_presigned_url(text_files[0].filename)


@pytest.mark.asyncio
async def test_generate_presigned_url_returns_none_on_non_existing_files(
    uow_cls: type[TestUOW],
):
    async with uow_cls() as uow:
        response = await uow.user_files.generate_presigned_url("NonExistingPath")
        assert len(response.results) == 1
        assert response.any_url is False
