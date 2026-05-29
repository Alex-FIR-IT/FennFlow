from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from fennflow._operations.context.create import CreateContext
from fennflow._operations.dto import OperationRecord
from fennflow._operations.enums import OperationTypeEnum
from fennflow._query_specs.select.get_visible import GetVisibleQuerySpec
from fennflow._sentinel import OMIT
from fennflow.backends.enums import OnConflictDoEnum
from fennflow.backends.exceptions import RecordAlreadyExistsException
from fennflow.repositories._validation_mixins.validate_duplicate import (
    ValidateDuplicatesMixin,
)
from fennflow.repositories.at import AtRepository

if TYPE_CHECKING:
    from fennflow._new_types import ConnectorExtra
    from fennflow.files.types import BinaryMedia
    from fennflow.responses.connector_raw import ConnectorRawResponse


class CreateRepository(
    AtRepository,
    ValidateDuplicatesMixin,
):
    """Repository for uploading (creating) files in the storage.

    This repository implements the "create" operation, which uploads new files
    to the configured storage (e.g. S3) within the current Unit of Work.

    **Behavior**:

    - Each file is registered in the backend as a pending operation
    - Files are uploaded via the connector
    - Backend commit is executed on uow.commit

    """

    async def create(
        self,
        *files: BinaryMedia,
        connector_extra: ConnectorExtra = OMIT,
    ) -> list[ConnectorRawResponse[Any]]:
        """Puts file if it doesn't exist in the backend.

        **Example**::

            file1 = TextContent.from_content("This is the first file.")
            await uow.user_files.at("user1/").create(file1)

        Raises:
            RecordAlreadyExistsException:
                If a file with the same path already exists in a backend
            FilepathsCollisionError:
                If files with the same filepath are passed
        """
        self.validate_duplicates_from_files(files)
        tasks = []
        operations = []
        for file in files:
            file._storage_prefix = self.cwd

            record = await self._uow._backend.backend_engine.execute(
                GetVisibleQuerySpec(
                    scope=self._uow._resolved_config.backend.scope,
                    namespace=self.repo_extra["namespace"],
                    storage_path=file.storage_path,
                    session_id=self._uow._session_id,
                )
            )

            if record:
                raise RecordAlreadyExistsException(
                    storage_path=record.storage_path,
                )

            operation = OperationRecord.from_uow(
                uow=self._uow,
                operation_type=OperationTypeEnum.CREATE,
                storage_path=file.storage_path,
                context=CreateContext(file=file),
                repo_extra=self.repo_extra,
            )

            await self._uow.backend.insert(
                operation,
                on_conflict=OnConflictDoEnum.REPLACE,
            )
            tasks.append(
                self._uow._operation_executor.execute(
                    operation,
                    connector_extra=connector_extra,
                ),
            )
            operations.append(operation)

        await self._uow.backend.flush(operations=operations)
        return await asyncio.gather(*tasks)
