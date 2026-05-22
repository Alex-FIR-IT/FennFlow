from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from typing_extensions import Self

from fennflow._datetime import AwareDatetime, now
from fennflow._operations.context.abstract import BaseContext
from fennflow._operations.enums import OperationStatusEnum, OperationTypeEnum
from fennflow._sentinel import OMIT, Omittable, is_given
from fennflow._shared import inserting_types
from fennflow._tmp_path_builder import TmpPathBuilder
from fennflow.backends.enums import OnConflictDoEnum

if TYPE_CHECKING:
    from fennflow import UnitOfWork
    from fennflow._new_types import BackendScope, Namespace, StoragePath
    from fennflow._operations.context.types import Context
    from fennflow.repositories.fields.base import RepoExtra


@dataclass(slots=True)
class Record:
    session_id: uuid.UUID
    storage_path: StoragePath
    scope: BackendScope
    namespace: Namespace
    operation_type: OperationTypeEnum
    status: OperationStatusEnum
    operation_id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: AwareDatetime = field(
        default_factory=now,
    )
    expired_at: AwareDatetime = field(
        default_factory=lambda: now() + datetime.timedelta(seconds=30)
    )
    error: str | None = None

    @property
    def is_pending(self) -> bool:
        return self.status == OperationStatusEnum.PENDING

    @property
    def is_uploaded(self) -> bool:
        return self.status == OperationStatusEnum.UPLOADED

    @property
    def is_failed(self) -> bool:
        return self.status == OperationStatusEnum.FAILED

    @property
    def is_deleted(self) -> bool:
        return self.status == OperationStatusEnum.DELETED

    @property
    def is_expired(self):
        return self.expired_at < now()

    @property
    def is_upserting_type(self) -> bool:
        return self.operation_type in inserting_types

    @property
    def is_put_type(self) -> bool:
        return self.operation_type == OperationTypeEnum.PUT

    def generate_tmp_path(self) -> StoragePath:
        return TmpPathBuilder.from_record(self)

    def mark_done(
        self,
    ) -> None:
        if self.operation_type in {
            OperationTypeEnum.CREATE,
            OperationTypeEnum.PUT,
        }:
            self.status = OperationStatusEnum.UPLOADED
        elif self.operation_type == OperationTypeEnum.DELETE:
            self.status = OperationStatusEnum.DELETED
        else:
            raise NotImplementedError(
                f"mark_done is not supported for {self.operation_type=}"
            )

    def mark_failed(
        self,
        error: str | None = None,
    ) -> None:
        self.status = OperationStatusEnum.FAILED
        self.error = error

    def mark_compensation_failed(
        self,
        error: str | None = None,
    ):
        self.status = OperationStatusEnum.COMPENSATION_FAILED
        self.error = error

    def mark_pending(
        self,
    ) -> None:
        self.status = OperationStatusEnum.PENDING

    def __hash__(self):
        return hash(self.storage_path)


@dataclass(slots=True)
class OperationRecord:
    record: Record
    repo_extra: RepoExtra
    context: Context = field(default_factory=BaseContext)
    on_conflict: OnConflictDoEnum = OnConflictDoEnum.RAISE

    @classmethod
    def create(
        cls,
        session_id: uuid.UUID,
        scope: BackendScope,
        storage_path: StoragePath,
        operation_type: OperationTypeEnum,
        repo_extra: RepoExtra,
        status: OperationStatusEnum = OperationStatusEnum.PENDING,
        context: Omittable[Context] = OMIT,
        on_conflict: OnConflictDoEnum = OnConflictDoEnum.RAISE,
    ) -> Self:
        record = Record(
            session_id=session_id,
            scope=scope,
            namespace=repo_extra["namespace"],
            storage_path=storage_path,
            operation_type=operation_type,
            status=status,
        )
        return cls(
            record=record,
            repo_extra=repo_extra,
            context=context if is_given(context) else BaseContext(),
            on_conflict=on_conflict,
        )

    @classmethod
    def from_uow(
        cls,
        uow: UnitOfWork,
        repo_extra: RepoExtra,
        storage_path: StoragePath,
        operation_type: OperationTypeEnum,
        status: OperationStatusEnum = OperationStatusEnum.PENDING,
        context: Omittable[Context] = OMIT,
    ) -> Self:
        return cls.create(
            session_id=uow._session_id,
            repo_extra=repo_extra,
            scope=uow._resolved_config.backend.scope,
            storage_path=storage_path,
            operation_type=operation_type,
            status=status,
            context=context,
        )

    @classmethod
    def from_record(cls, record: Record) -> Self:
        return cls(record=record, repo_extra={"namespace": record.namespace})
