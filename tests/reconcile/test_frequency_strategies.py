from uuid import uuid4

import pytest

from fennflow import ConfigDict, UnitOfWork
from fennflow._operations.dto import OperationRecord
from fennflow._operations.enums import OperationStatusEnum, OperationTypeEnum
from fennflow._query_specs.insert.insert import InsertQuerySpec
from fennflow.connectors import InMemoryConnector
from fennflow.reconciler import (
    ReconcileConfig,
    ReconcileFrequencyEnum,
    ReconcileStrategyEnum,
)
from fennflow.repositories import RepoField
from tests.shared.repositories import UserFiles


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "frequency, strategy, prefill_backend, response_len, files_assertion",
    [
        # ON_START_APP combinations
        (
            ReconcileFrequencyEnum.ON_START_APP,
            ReconcileStrategyEnum.FILL_IF_EMPTY,
            False,
            2,
            True,
        ),
        (
            ReconcileFrequencyEnum.ON_START_APP,
            ReconcileStrategyEnum.FILL_IF_EMPTY,
            True,
            1,
            False,
        ),
        (
            ReconcileFrequencyEnum.ON_START_APP,
            ReconcileStrategyEnum.REPLACE,
            False,
            2,
            True,
        ),
        (
            ReconcileFrequencyEnum.ON_START_APP,
            ReconcileStrategyEnum.REPLACE,
            True,
            2,
            True,
        ),
        (
            ReconcileFrequencyEnum.ON_START_APP,
            ReconcileStrategyEnum.INSERT_MISSING,
            False,
            2,
            True,
        ),
        (
            ReconcileFrequencyEnum.ON_START_APP,
            ReconcileStrategyEnum.INSERT_MISSING,
            True,
            2,
            True,
        ),
        # ON_SESSION_START combinations
        (
            ReconcileFrequencyEnum.ON_SESSION_START,
            ReconcileStrategyEnum.FILL_IF_EMPTY,
            False,
            2,
            True,
        ),
        (
            ReconcileFrequencyEnum.ON_SESSION_START,
            ReconcileStrategyEnum.FILL_IF_EMPTY,
            True,
            1,
            False,
        ),
        (
            ReconcileFrequencyEnum.ON_SESSION_START,
            ReconcileStrategyEnum.REPLACE,
            False,
            2,
            True,
        ),
        (
            ReconcileFrequencyEnum.ON_SESSION_START,
            ReconcileStrategyEnum.REPLACE,
            True,
            2,
            True,
        ),
        (
            ReconcileFrequencyEnum.ON_SESSION_START,
            ReconcileStrategyEnum.INSERT_MISSING,
            False,
            2,
            True,
        ),
        (
            ReconcileFrequencyEnum.ON_SESSION_START,
            ReconcileStrategyEnum.INSERT_MISSING,
            True,
            2,
            True,
        ),
        # NEVER combinations
        (
            ReconcileFrequencyEnum.NEVER,
            ReconcileStrategyEnum.FILL_IF_EMPTY,
            False,
            0,
            False,
        ),
        (
            ReconcileFrequencyEnum.NEVER,
            ReconcileStrategyEnum.FILL_IF_EMPTY,
            True,
            1,
            False,
        ),
        (
            ReconcileFrequencyEnum.NEVER,
            ReconcileStrategyEnum.REPLACE,
            False,
            0,
            False,
        ),
        (
            ReconcileFrequencyEnum.NEVER,
            ReconcileStrategyEnum.REPLACE,
            True,
            1,
            False,
        ),
        (
            ReconcileFrequencyEnum.NEVER,
            ReconcileStrategyEnum.INSERT_MISSING,
            False,
            0,
            False,
        ),
        (
            ReconcileFrequencyEnum.NEVER,
            ReconcileStrategyEnum.INSERT_MISSING,
            True,
            1,
            False,
        ),
    ],
)
async def test_reconcile_on_non_empty_connector(
    frequency,
    strategy,
    prefill_backend,
    response_len,
    files_assertion,
    text_files,
    namespace,
    scope,
    uow_cls,
):

    class TestUOW(UnitOfWork):
        user_files = RepoField(UserFiles, namespace=namespace)
        config = ConfigDict(
            reconcile=ReconcileConfig(frequency=frequency, strategy=strategy),
            backend=uow_cls.config["backend"],
            connector=uow_cls.config["connector"],
        )

    if prefill_backend:
        async with uow_cls() as uow:
            await uow.backend.backend_engine.execute(
                InsertQuerySpec.from_operations(
                    operations=[
                        OperationRecord.create(
                            session_id=uuid4(),
                            storage_path=text_files[0].filename,
                            status=OperationStatusEnum.UPLOADED,
                            operation_type=OperationTypeEnum.CREATE,
                            repo_extra=TestUOW.user_files.repo_extra,
                            scope=scope,
                        )
                    ]
                )
            )

    for text_file in text_files:
        InMemoryConnector._storage[namespace][text_file.filename] = text_file

    async with TestUOW() as uow:
        response = await uow.user_files.list()

        assert len(response) == response_len

        files = []
        for storage_path in response:
            response = await uow.user_files.get(storage_path)
            files.extend(response)

        files_equal = sorted(files) == sorted(text_files)
        assert files_equal == files_assertion
