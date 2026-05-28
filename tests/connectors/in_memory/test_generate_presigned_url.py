import pytest

from fennflow.connectors.exceptions import ConnectorCapabilityException


@pytest.mark.asyncio
async def test_generate_presigned_url_raises_capability_error(uow_cls):
    async with uow_cls() as uow:
        with pytest.raises(ConnectorCapabilityException):
            await uow.user_files.generate_presigned_url("")
