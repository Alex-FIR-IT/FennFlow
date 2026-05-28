import uuid

import aiobotocore.session
import pytest
import pytest_asyncio

from fennflow._new_types import BackendScope, Namespace
from fennflow._operations.dto import OperationRecord, Record
from fennflow._operations.enums import OperationStatusEnum, OperationTypeEnum
from fennflow.files import TextContent
from tests.shared.constants import NAMESPACE, PYTEST_USE_MINIO, SCOPE
from tests.shared.uows import MinioUOW, TestUOW
from tests.utils import reset_state

params = [TestUOW]
ids = ["sqlite_in_memory"]

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


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_minio_bucket():

    if not PYTEST_USE_MINIO:
        return

    session = aiobotocore.session.get_session()
    async with session.create_client("s3") as client:
        try:
            await client.create_bucket(Bucket=NAMESPACE)
        except client.exceptions.BucketAlreadyOwnedByYou:
            pass
