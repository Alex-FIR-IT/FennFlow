from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from fennflow._datetime import now
from fennflow._operations.context.abstract import BaseContext
from fennflow._operations.enums import OperationStatusEnum, OperationTypeEnum
from fennflow._operations.tmp_path_builder import TmpPathBuilder
from fennflow._sentinel import NOT_GIVEN
from fennflow.backends.enums import OnConflictDoEnum

if TYPE_CHECKING:
    from fennflow._new_types import Namespace, StoragePath
    from fennflow._operations.context.types import Context
    from fennflow._sentinel import NotGiven
    from fennflow.repositories.fields.base import RepoExtra


@dataclass(slots=True)
class OperationRecord:
    session_id: uuid.UUID
    storage_path: StoragePath
    repo_extra: RepoExtra
    operation_type: OperationTypeEnum
    status: OperationStatusEnum
    context: Context = field(default_factory=BaseContext)
    operation_id: uuid.UUID = field(default_factory=uuid.uuid4)
    on_conflict: OnConflictDoEnum = OnConflictDoEnum.RAISE
    created_at: datetime.datetime = field(
        default_factory=now,
    )
    expired_at: datetime.datetime = field(
        default_factory=lambda: now() + datetime.timedelta(seconds=30)
    )
    error: str | None | NotGiven = NOT_GIVEN

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
    def namespace(self) -> Namespace:
        return self.repo_extra["namespace"]

    @property
    def is_expired(self):
        return self.expired_at < now()

    @property
    def is_dangling(self) -> bool:
        return self.is_expired and not self.is_uploaded

    def is_locked(self, current_session_id: UUID) -> bool:
        return (
            self.session_id != current_session_id
            and self.is_pending
            and not self.is_expired
        )

    def is_visible(self, requested_from_session_id: UUID) -> bool:
        return self.is_uploaded or (
            self.is_pending
            and self.session_id == requested_from_session_id
            and self.is_upserting_type
        )

    @property
    def is_upserting_type(self) -> bool:
        return self.operation_type in {
            OperationTypeEnum.CREATE,
            OperationTypeEnum.PUT,
        }

    @property
    def is_put_type(self) -> bool:
        return self.operation_type == OperationTypeEnum.PUT

    def generate_tmp_path(self) -> StoragePath:
        return TmpPathBuilder.from_operation(self)

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
