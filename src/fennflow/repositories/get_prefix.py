from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fennflow.repositories._helper_mixins import paths

from .._sentinel import OMIT
from . import GetRepository
from .at import AtRepository

if TYPE_CHECKING:
    from .._new_types import ConnectorExtra, StoragePath
    from ..responses.media import MediaResponse


class GetPrefixRepository(AtRepository):
    """Repository mixin for getting files from storage by prefix.

    Combines ListRepository and GetRepository.
    """

    async def get_prefix(
        self,
        prefix: str,
        *,
        connector_extra: ConnectorExtra = OMIT,
    ) -> MediaResponse[Any]:
        """Get files from storage by prefix.

        Args:
            prefix: Prefix files relative to the current directory.
            connector_extra: Additional kwargs forwarded to the connector.

        Returns:
            MediaResponse

        **Example**::

            async with UOW() as uow:
                await uow.user_files.get_prefix("some_prefix")
        """
        storage_paths: list[StoragePath] = await paths.get_all_paths(
            repository=self,
            prefix=prefix,
        )

        get_repository = GetRepository(
            uow=self._uow,
            path="",
            repo_extra=self.repo_extra,
        )
        return await get_repository.get(*storage_paths, connector_extra=connector_extra)
