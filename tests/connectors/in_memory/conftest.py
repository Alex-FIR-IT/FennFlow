import pytest_asyncio

from tests.shared.uows import TestUOW
from tests.utils import reset_state


@pytest_asyncio.fixture(
    params=[TestUOW],
    ids=["sqlite_in_memory"],
)
async def uow_cls(request, scope):
    cls = request.param
    await reset_state(cls, scope)
    yield cls
