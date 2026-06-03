from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._sentinel import OMIT
from fennflow.repositories._helper_mixins import paths

from .at import AtRepository
from .delete import DeleteRepository

if TYPE_CHECKING:
    from .._new_types import ConnectorExtra, StoragePath
    from .delete import DeleteResponse


class DeletePrefixRepository(AtRepository):
    """Repository mixin for deleting files from storage by prefix.

    Implements Saga-based deletion with automatic compensation on failure.
    """

    async def delete_prefix(
        self,
        prefix: str,
        *,
        connector_extra: ConnectorExtra = OMIT,
    ) -> DeleteResponse:
        """Delete files from storage by prefix.

        Args:
            prefix: Prefix files relative to the current directory.
            connector_extra: Additional kwargs forwarded to the connector.

        Returns:
            DeleteResponse containing a result per path in the same order
            as it was listed.
            Each element is a ConnectorRawResponse.

        **Example**::

            async with UOW() as uow:
                await uow.user_files.delete_prefix() # deletes all files in the bucket
        """
        storage_paths: list[StoragePath] = await paths.get_all_paths(
            repository=self,
            prefix=prefix,
        )

        delete_repository = DeleteRepository(
            uow=self._uow,
            path="",
            repo_extra=self.repo_extra,
        )
        return await delete_repository.delete(
            *storage_paths,
            connector_extra=connector_extra,
        )
