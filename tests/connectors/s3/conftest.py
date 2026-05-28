import pytest_asyncio

from tests.shared.uows import MinioUOW
from tests.utils import reset_state


@pytest_asyncio.fixture(
    params=[MinioUOW],
    ids=["minio"],
)
async def uow_cls(request, scope):
    cls = request.param
    await reset_state(cls, scope)
    yield cls
