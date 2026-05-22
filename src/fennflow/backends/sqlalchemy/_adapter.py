from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fennflow._operations.dto import Record
from fennflow._operations.enums import OperationStatusEnum, OperationTypeEnum

if TYPE_CHECKING:
    from fennflow.backends.sqlalchemy import AbstractOperationRecordModel


@dataclass(slots=True, frozen=True)
class RecordOrmAdapter:
    orm_model: type[AbstractOperationRecordModel]

    def to_orm(self, record: Record):
        return self.orm_model(
            operation_id=record.operation_id,
            session_id=record.session_id,
            scope=record.scope,
            namespace=record.namespace,
            storage_path=record.storage_path,
            operation_type=record.operation_type.value,
            status=record.status.value,
            created_at=record.created_at,
            expired_at=record.expired_at,
            error=record.error,
        )

    def from_orm(self, orm_obj: AbstractOperationRecordModel) -> Record:

        return Record(
            operation_id=orm_obj.operation_id,
            session_id=orm_obj.session_id,
            scope=orm_obj.scope,
            namespace=orm_obj.namespace,
            storage_path=orm_obj.storage_path,
            operation_type=OperationTypeEnum(orm_obj.operation_type),
            status=OperationStatusEnum(orm_obj.status),
            created_at=orm_obj.created_at,
            expired_at=orm_obj.expired_at,
            error=orm_obj.error,
        )
