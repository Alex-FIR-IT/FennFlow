import pytest
import pytest_asyncio

from fennflow import ConfigDict
from fennflow.backends import InMemoryBackendConfig
from fennflow.connectors import InMemoryConnector, InMemoryConnectorConfig
from fennflow.files import TextContent
from fennflow.reconciler._orchestrator import ReconcileOrchestrator
from fennflow.repositories import (
    CreateRepository,
    DeleteRepository,
    GetRepository,
    RepoField,
)
from fennflow.repositories.list import ListRepository
from fennflow.repositories.put import PutRepository
from fennflow.uow import UnitOfWork


class UserFiles(
    PutRepository,
    CreateRepository,
    DeleteRepository,
    GetRepository,
    ListRepository,
):
    pass


class TestUOW(UnitOfWork):
    user_files = RepoField(UserFiles, namespace="user_files")
    config = ConfigDict(
        backend=InMemoryBackendConfig(),
        connector=InMemoryConnectorConfig(),
    )


class TestSqliteUOW(UnitOfWork):
    user_files = RepoField(UserFiles, namespace="user_files")
    config = ConfigDict(
        backend=InMemoryBackendConfig(),
        connector=InMemoryConnectorConfig(),
    )


@pytest.fixture(
    params=[
        TestUOW,
        # TestSqliteUOW,
    ],
    ids=[
        "memory",
        # "sqlite",
    ],
)
def uow_cls(request):
    return request.param


@pytest.fixture
def scope(uow_cls) -> BackendScope:
    return uow_cls.config["backend"].scope


@pytest.fixture
def namespace(uow_cls) -> Namespace:
    return uow_cls.user_files.repo_extra["namespace"]


@pytest.fixture
def text_files():
    return [
        TextContent.from_content("hello"),
        TextContent.from_content("world"),
    ]


@pytest_asyncio.fixture(autouse=True)
async def reset_inmemory_state(uow_cls):
    async with uow_cls() as uow:
        uow._backend.backend_engine.clear()

    InMemoryConnector.drop_all()
    ReconcileOrchestrator._reconciled_on_startup = set()
