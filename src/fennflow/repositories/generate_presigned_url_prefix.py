from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._sentinel import OMIT, Omittable
from fennflow.repositories import GeneratePresignedUrlRepository
from fennflow.repositories._helper_mixins import paths
from fennflow.repositories.at import AtRepository

if TYPE_CHECKING:
    from fennflow._new_types import ConnectorExtra, StoragePath
    from fennflow.responses.presigned_url import PresignedUrlResponse


class GeneratePresignedUrlPrefixRepository(AtRepository):
    """Repository mixin for generating presigned urls by prefix.

    Combines ListRepository and GeneratePresignedUrlRepository.
    """

    async def generate_presigned_url_prefix(
        self,
        prefix: str,
        *,
        expires_in: Omittable[int] = OMIT,
        connector_extra: ConnectorExtra = OMIT,
    ) -> PresignedUrlResponse:
        """Generate a presigned URLs for the given prefix.

        Does not interact with the backend or file storage.
        No Saga compensation is applied.

        Args:
            prefix: Prefix files relative to the current directory.
            expires_in: Expiry duration in seconds. When omitted, the
                connector's default is used.
            connector_extra: Additional kwargs forwarded to the connector.

        Returns:
            PresignedUrlResponse containing the generated URLs.

        Raises:
            ConnectorCapabilityException: If the configured connector
                does not support presigned URL generation.

        **Example**::

            async with UOW() as uow:
                response = await uow.files.generate_presigned_url("user1/"
                    expires_in=600,
                )
                print(response.results) # list[str | None]
                print(list(response.urls)) # list[str]
        """
        storage_paths: list[StoragePath] = await paths.get_all_paths(
            repository=self,
            prefix=prefix,
        )

        generate_presigned_url_repo = GeneratePresignedUrlRepository(
            uow=self._uow,
            path="",
            repo_extra=self.repo_extra,
        )
        return await generate_presigned_url_repo.generate_presigned_url(
            *storage_paths,
            expires_in=expires_in,
            connector_extra=connector_extra,
        )
