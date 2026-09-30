from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TypeVar

from fennflow._operations.dto import Record
from fennflow._operations.enums import OperationStatusEnum, OperationTypeEnum
from fennflow.backends.sqlalchemy._base import (
    AbstractOperationRecordModel,
    AbstractOutboxTable,
)

OrmModel = TypeVar("OrmModel")
DTO = TypeVar("DTO")


class AdapterProtocol(Protocol[OrmModel, DTO]):
    @property
    def orm_model(self) -> type[OrmModel]: ...

    @property
    def dto(self) -> type[DTO]: ...

    def to_orm(
        self,
        record: DTO,
    ) -> OrmModel: ...

    @staticmethod
    def from_orm(
        orm_obj: OrmModel,
    ) -> DTO: ...


@dataclass(slots=True, frozen=True)
class RecordOrmAdapter(AdapterProtocol[AbstractOperationRecordModel, Record]):
    orm_model: type[AbstractOperationRecordModel]
    dto: type[Record]

    def to_orm(
        self,
        record: Record,
    ):
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

    @staticmethod
    def from_orm(
        orm_obj: AbstractOperationRecordModel,
    ) -> Record:
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


@dataclass(slots=True, frozen=True)
class OutboxRecordOrmAdapter(AdapterProtocol[AbstractOutboxTable, Record]):
    orm_model: type[AbstractOutboxTable]
    dto: type[Record]

    def to_orm(
        self,
        record: Record,
    ):
        return self.orm_model(
            event_id=record.operation_id,
            aggregate_type=record.aggregate_type,
            aggregate_id=record.aggregate_id,
            event_type=record.operation_type,
            payload={
                "operation_id": record.operation_id.hex,
                "operation_type": record.operation_type.value,
                "session_id": record.session_id.hex,
                "scope": record.scope,
                "namespace": record.namespace,
                "storage_path": record.storage_path,
                "status": record.status.value,
                "created_at": record.created_at.isoformat(),
                "expired_at": record.expired_at.isoformat(),
                "error": record.error,
            },
        )

    @staticmethod
    def from_orm(
        orm_obj: AbstractOutboxTable,
    ) -> Record:
        return Record(
            operation_id=orm_obj.event_id,
            session_id=orm_obj.payload["session_id"],
            scope=orm_obj.payload["scope"],
            namespace=orm_obj.payload["namespace"],
            storage_path=orm_obj.payload["storage_path"],
            operation_type=OperationTypeEnum(orm_obj.event_type),
            status=OperationStatusEnum(orm_obj.payload["status"]),
            created_at=orm_obj.payload["created_at"],
            expired_at=orm_obj.payload["expiry_at"],
            error=orm_obj.payload["error"],
        )
