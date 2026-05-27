from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fennflow._sentinel import OMIT, Omittable
from fennflow.repositories.at import AtRepository

if TYPE_CHECKING:
    from fennflow.files.responses.presigned_url import PresignedUrlResponse


class GeneratePresignedUrlRepository(AtRepository):
    """Repository mixin for generating presigned URLs.

    Provides access to connector-level presigned URL generation
    without touching the backend or file storage.

    Note:
        This mixin is only supported by connectors that implement
        presigned URL generation (e.g. S3Connector).
        Using it with InMemoryConnector or LocalConnector will raise
        ConnectorCapabilityException.
    """

    async def generate_presigned_url(
        self,
        storage_path: str,
        *,
        expires_in: Omittable[int] = OMIT,
        connector_extra: Omittable[Any] = OMIT,
    ) -> PresignedUrlResponse:
        """Generate a presigned URL for the given path.

        Does not interact with the backend or file storage.
        No Saga compensation is applied.

        Args:
            storage_path: Path to the file relative to the current directory.
            expires_in: Expiry duration in seconds. When omitted, the
                connector's default is used.
            connector_extra: Additional connector-specific parameters
                passed directly to the connector.

        Returns:
            PresignedUrlResponse containing the generated URL.

        Raises:
            ConnectorCapabilityException: If the configured connector
                does not support presigned URL generation.

        **Example**::

            async with UOW() as uow:
                response = await uow.files.at("user1/").generate_presigned_url(
                    "report.pdf",
                    expires_in=600,
                )
                print(response.url)
        """
        storage_path = self._join_path(storage_path)

        return await self._uow.connector.generate_presigned_url(
            storage_path=storage_path,
            expires_in=expires_in,
            repo_extra=self.repo_extra,
            connector_extra=connector_extra,
        )
