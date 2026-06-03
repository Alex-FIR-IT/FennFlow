from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fennflow._sentinel import OMIT, Omittable
from fennflow.repositories._helper_mixins import gather_tasks, visible_record
from fennflow.repositories.at import AtRepository
from fennflow.responses.presigned_url import PresignedUrlResponse

if TYPE_CHECKING:
    from collections.abc import Coroutine


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
        *storage_paths: str,
        expires_in: Omittable[int] = OMIT,
        connector_extra: Omittable[Any] = OMIT,
    ) -> PresignedUrlResponse:
        """Generate a presigned URL for the given path.

        Does not interact with the backend or file storage.
        No Saga compensation is applied.

        Args:
            storage_paths: Paths to the files relative to the current directory.
            expires_in: Expiry duration in seconds. When omitted, the
                connector's default is used.
            connector_extra: Additional connector-specific parameters
                passed directly to the connector.

        Returns:
            PresignedUrlResponse containing the generated URLs.

        Raises:
            ConnectorCapabilityException: If the configured connector
                does not support presigned URL generation.

        **Example**::

            async with UOW() as uow:
                response = await uow.files.at("user1/").generate_presigned_url(
                    "report.pdf",
                    "NonExistingFile",
                    expires_in=600,
                )
                print(response.results) # [<Link>, None]
                print(list(response.urls)) # [<Link>]
        """
        tasks = []
        task_indexes = []
        results: list[None | str] = [None] * len(storage_paths)

        for task_idx, relative_path in enumerate(storage_paths):
            storage_path = self._join_path(relative_path)

            record = await visible_record.get_visible_record(
                repostory=self,
                storage_path=storage_path,
            )

            if record is None:
                continue

            tasks.append(
                self._uow.connector.generate_presigned_url(
                    storage_path=storage_path,
                    expires_in=expires_in,
                    repo_extra=self.repo_extra,
                    connector_extra=connector_extra,
                )
            )
            task_indexes.append(task_idx)

        return await self.__construct_response(
            tasks=tasks,
            task_indexes=task_indexes,
            results=results,
        )

    async def __construct_response(
        self,
        tasks: list[Coroutine[Any, Any, str]],
        task_indexes: list[int],
        results: list[None | str],
    ) -> PresignedUrlResponse:
        results = await gather_tasks.gather_tasks(
            tasks=tasks,
            task_indexes=task_indexes,
            results=results,
        )
        return PresignedUrlResponse(results=results)
