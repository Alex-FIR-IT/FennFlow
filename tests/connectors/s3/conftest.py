import pytest_asyncio

from tests.shared.constants import PYTEST_USE_MINIO
from tests.shared.uows import MinioUOW
from tests.utils import reset_state

params = []
ids = []

if PYTEST_USE_MINIO:
    params.append(MinioUOW)
    ids.append("minio")


@pytest_asyncio.fixture(
    params=params,
    ids=ids,
)
async def uow_cls(request, scope):
    cls = request.param
    await reset_state(cls, scope)
    yield cls
