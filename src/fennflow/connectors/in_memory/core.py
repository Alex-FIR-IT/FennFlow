from __future__ import annotations

import bisect
import logging
from collections import defaultdict
from itertools import islice
from typing import TYPE_CHECKING, Any, NoReturn

from fennflow._decorators import reraise_with
from fennflow._sentinel import OMIT, Omittable
from fennflow.connectors._abstract import AbstractConnector
from fennflow.connectors.exceptions import (
    ConnectorCapabilityException,
    NoSuchKeyException,
)
from fennflow.files import ContentFactory
from fennflow.responses.connector_list import ConnectorListResponse
from fennflow.responses.connector_raw import ConnectorRawResponse
from fennflow.responses.content import ContentResponse
from fennflow.responses.media import MediaResponse

if TYPE_CHECKING:
    from typing_extensions import Self

    from fennflow._new_types import ConnectorExtra, Namespace, StoragePath
    from fennflow.connectors._abstract.base import RepoExtraType
    from fennflow.connectors.in_memory.config import InMemoryConnectorConfig
    from fennflow.files.types import BinaryMedia
    from fennflow.repositories.fields.base import RepoExtra

logger = logging.getLogger(__name__)


class InMemoryConnector(AbstractConnector):
    """In-memory connector for file storage, primarily used for testing.

    Stores files in a class-level dictionary shared across all instances,

    Use ``drop_all()`` between tests to reset state.

    Example::

        class UOW(UnitOfWork):
            config = ConfigDict(
                connector=InMemoryConnectorConfig(),
            )
    """

    _storage: defaultdict[Namespace, dict[StoragePath, BinaryMedia]] | None = None

    async def open(self) -> Self:
        return self

    async def close(self):
        pass

    def __init__(self, config: InMemoryConnectorConfig):
        self._config = config

        if self.__class__._storage is None:
            self.__class__._storage = defaultdict(dict)

    @property
    def storage(
        self,
    ) -> defaultdict[Namespace, dict[StoragePath, BinaryMedia]]:
        if self.__class__._storage is None:
            raise RuntimeError(
                "Cannot get in-memory storage. InMemoryConnector is not initialized.",
            )
        return self.__class__._storage

    async def put(
        self,
        file: BinaryMedia,
        repo_extra: RepoExtra,
        connector_extra: ConnectorExtra = OMIT,  # noqa: ARG002
    ) -> None:
        namespace = repo_extra["namespace"]
        self.storage[namespace][file.storage_path] = file
        logger.debug(f"{file=} uploaded to {namespace=}")

    async def get(
        self,
        storage_path: StoragePath,
        repo_extra: RepoExtra,
        connector_extra: ConnectorExtra = OMIT,  # noqa: ARG002
    ) -> MediaResponse[None]:

        if storage_path not in self.storage[repo_extra["namespace"]]:
            return MediaResponse()

        file = self.storage[repo_extra["namespace"]][storage_path]

        content_response = ContentResponse(
            raw_response=None,
            content=ContentFactory.from_bytes(
                media_type=file.media_type,
                data=file.data,
                **file.get_metadata(),
            ),
        )

        return MediaResponse.from_content_response(response=content_response)

    async def delete(
        self,
        storage_path: StoragePath,
        repo_extra: RepoExtra,
        connector_extra: ConnectorExtra = OMIT,  # noqa: ARG002
    ) -> ConnectorRawResponse[None]:
        self.storage[repo_extra["namespace"]].pop(storage_path, None)

        return ConnectorRawResponse(raw_response=None)

    @reraise_with(NoSuchKeyException(), catch=KeyError)
    async def copy_object(
        self,
        repo_extra: RepoExtra,
        from_storage_path: StoragePath,
        to_storage_path: StoragePath,
        to_namespace: Namespace,
        connector_extra: ConnectorExtra = OMIT,  # noqa: ARG002
    ) -> ConnectorRawResponse[None]:
        file = self.storage[repo_extra["namespace"]][from_storage_path]
        self.storage[to_namespace][to_storage_path] = file

        return ConnectorRawResponse(raw_response=None)

    @classmethod
    def drop_all(cls) -> None:
        cls._storage = defaultdict(dict)

    async def list_objects(
        self,
        prefix: str,
        repo_extra: RepoExtraType,
        limit: int = 1000,
        continuation_token: Omittable[str] | None = OMIT,
        connector_extra: ConnectorExtra = OMIT,  # noqa: ARG002
    ) -> ConnectorListResponse[None]:
        filtered_storage_paths = []
        all_storage_paths = sorted(self.storage[repo_extra["namespace"]])

        if continuation_token:
            index = bisect.bisect_right(all_storage_paths, continuation_token)
        else:
            index = 0

        for storage_path in islice(all_storage_paths, index, None):
            if 0 >= limit:
                continuation_token = storage_path
                break

            if storage_path.startswith(prefix):
                filtered_storage_paths.append(storage_path)
                limit -= 1
        else:
            continuation_token = None

        return ConnectorListResponse(
            storage_paths=filtered_storage_paths,
            continuation_token=continuation_token,
            raw_response=None,
        )

    async def generate_presigned_url(
        self,
        storage_path: str,  # noqa: ARG002
        repo_extra: RepoExtraType,  # noqa: ARG002
        expires_in: Omittable[int] = OMIT,  # noqa: ARG002
        connector_extra: Omittable[Any] = OMIT,  # noqa: ARG002
    ) -> NoReturn:
        raise ConnectorCapabilityException("generate_presigned_url")
