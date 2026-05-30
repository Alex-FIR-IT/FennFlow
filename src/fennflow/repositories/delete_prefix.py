from __future__ import annotations

from typing import TYPE_CHECKING

from .._sentinel import OMIT, Omittable
from .delete import DeleteRepository
from .list import ListRepository

if TYPE_CHECKING:
    from .._new_types import ConnectorExtra, StoragePath
    from .delete import DeleteResponse


class DeletePrefixRepository(DeleteRepository, ListRepository):
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
        paths: list[StoragePath] = await self.__get_all_paths(prefix=prefix)

        storage = self._cd_root()
        return await storage.delete(*paths, connector_extra=connector_extra)

    async def __get_all_paths(self, prefix: str) -> list[StoragePath]:
        continue_flag = True
        continuation_token: Omittable[str] = OMIT
        paths: list[str] = []

        while continue_flag:
            list_response = await self.list(
                prefix=prefix,
                continuation_token=continuation_token,
            )
            paths.extend(list_response)
            continuation_token = list_response.continuation_token or OMIT

            continue_flag = bool(list_response.continuation_token)

        return paths
