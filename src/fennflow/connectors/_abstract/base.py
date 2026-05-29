from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from fennflow._sentinel import OMIT, Omittable
from fennflow.repositories.fields.base import RepoExtra

if TYPE_CHECKING:
    from typing_extensions import Self

    from fennflow._new_types import ConnectorExtra, Namespace, StoragePath
    from fennflow.files.types import BinaryMedia
    from fennflow.responses.list import ListResponse
    from fennflow.responses.media import MediaResponse
    from fennflow.responses.presigned_url import PresignedUrlResponse

RepoExtraType = TypeVar("RepoExtraType", bound=RepoExtra)


class AbstractConnector(ABC, Generic[RepoExtraType]):
    """Base class for all FennFlow storage connectors.

    A connector is responsible for performing actual file operations
    against a storage backend (e.g. S3, local filesystem, in-memory).
    All operations are async and integrate with the Saga execution flow
    via ``OperationExecutor``.

    To implement a custom connector, subclass this and implement all
    abstract methods. Register it in ``connector_registry`` to make it
    available via ``ConnectorFactory``.
    """

    @abstractmethod
    async def open(self) -> Self:
        """Initialize the connector and return self."""

    @abstractmethod
    async def close(self) -> Any:
        """Clean up resources."""

    @abstractmethod
    async def put(
        self,
        file: BinaryMedia,
        repo_extra: RepoExtraType,
        connector_extra: ConnectorExtra = OMIT,
    ) -> Any:
        """Upload a file to storage."""

    @abstractmethod
    async def get(
        self,
        storage_path: StoragePath,
        repo_extra: RepoExtraType,
        connector_extra: ConnectorExtra = OMIT,
    ) -> MediaResponse:
        """Download a file from storage."""

    @abstractmethod
    async def delete(
        self,
        storage_path: StoragePath,
        repo_extra: RepoExtraType,
        connector_extra: ConnectorExtra = OMIT,
    ):
        """Delete a file from storage."""

    @abstractmethod
    async def copy_object(
        self,
        repo_extra: RepoExtraType,
        from_storage_path: StoragePath,
        to_storage_path: StoragePath,
        to_namespace: Namespace,
        connector_extra: ConnectorExtra = OMIT,
    ):
        """Copy a file within or across namespaces."""

    @abstractmethod
    async def list_objects(
        self,
        prefix: str,
        repo_extra: RepoExtraType,
        limit: int = 1000,
        continuation_token: Omittable[str] | None = OMIT,
        connector_extra: ConnectorExtra = OMIT,
    ) -> ListResponse:
        """List all files in storage."""

    @abstractmethod
    async def generate_presigned_url(
        self,
        storage_path: str,
        repo_extra: RepoExtraType,
        expires_in: Omittable[int] = OMIT,
        connector_extra: ConnectorExtra = OMIT,
    ) -> PresignedUrlResponse:
        """Generate a presigned url."""
