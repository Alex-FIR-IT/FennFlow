import pytest
import pytest_asyncio

from fennflow import ConfigDict
from fennflow._new_types import BackendScope, Namespace
from fennflow.backends import InMemoryBackendConfig
from fennflow.backends.sqlalchemy.config import SqlalchemyBackendConfig
from fennflow.connectors import InMemoryConnectorConfig
from fennflow.files import TextContent
from fennflow.repositories import (
    CreateRepository,
    DeleteRepository,
    GetRepository,
    RepoField,
)
from fennflow.repositories.list import ListRepository
from fennflow.repositories.put import PutRepository
from fennflow.uow import UnitOfWork
from tests.shared import NAMESPACE, SCOPE
from tests.utils import reset_state


class UserFiles(
    PutRepository,
    CreateRepository,
    DeleteRepository,
    GetRepository,
    ListRepository,
):
    pass


class TestUOW(UnitOfWork):
    user_files = RepoField(UserFiles, namespace=NAMESPACE)
    config = ConfigDict(
        backend=InMemoryBackendConfig(),
        connector=InMemoryConnectorConfig(),
    )


class TestSqliteUOW(UnitOfWork):
    user_files = RepoField(UserFiles, namespace=NAMESPACE)
    config = ConfigDict(
        backend=SqlalchemyBackendConfig(scope=SCOPE),
        connector=InMemoryConnectorConfig(),
    )


@pytest.fixture(
    params=[
        TestUOW,
        TestSqliteUOW,
    ],
    ids=[
        "memory",
        "sqlite",
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
async def reset_state_fixture(uow_cls, scope):
    await reset_state(uow_cls, scope)


@pytest_asyncio.fixture
def operations(namespace: str, scope: str):
    operations = []
    for i in range(10):
        record = Record(
            session_id=uuid.uuid4(),
            storage_path=f"path/{i}.txt",
            scope=scope,
            namespace=namespace,
            operation_type=OperationTypeEnum.CREATE,
            status=OperationStatusEnum.PENDING,
        )
        operations.append(OperationRecord.from_record(record))

    return operations
