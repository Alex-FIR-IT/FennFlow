import uuid

import pytest
import pytest_asyncio

from fennflow import ConfigDict
from fennflow._new_types import BackendScope, Namespace
from fennflow._operations.dto import OperationRecord, Record
from fennflow._operations.enums import OperationStatusEnum, OperationTypeEnum
from fennflow.backends import InMemoryBackendConfig
from fennflow.connectors import InMemoryConnectorConfig
from fennflow.files import TextContent
from fennflow.repositories import (
    CreateRepository,
    DeleteRepository,
    GeneratePresignedUrlRepository,
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
    GeneratePresignedUrlRepository,
):
    pass


class TestUOW(UnitOfWork):
    user_files = RepoField(UserFiles, namespace=NAMESPACE)
    config = ConfigDict(
        backend=InMemoryBackendConfig(scope=SCOPE),
        connector=InMemoryConnectorConfig(),
    )


@pytest.fixture(
    params=[TestUOW],
    ids=["sqlite_in_memory"],
)
def uow_cls(request):
    return request.param


@pytest.fixture
def scope() -> BackendScope:
    return SCOPE


@pytest.fixture
def namespace() -> Namespace:
    return NAMESPACE


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
    operations: list[OperationRecord] = []
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
