from fennflow import ConfigDict, UnitOfWork
from fennflow.backends import InMemoryBackendConfig
from fennflow.connectors import InMemoryConnectorConfig, S3ConnectorConfig
from fennflow.repositories import RepoField
from tests.shared.constants import NAMESPACE, SCOPE
from tests.shared.repositories import UserFiles


class TestUOW(UnitOfWork):
    user_files = RepoField(UserFiles, namespace=NAMESPACE)
    config = ConfigDict(
        backend=InMemoryBackendConfig(scope=SCOPE),
        connector=InMemoryConnectorConfig(),
    )


class MinioUOW(TestUOW):
    config = ConfigDict(
        backend=InMemoryBackendConfig(scope=SCOPE),
        connector=S3ConnectorConfig(),
    )
