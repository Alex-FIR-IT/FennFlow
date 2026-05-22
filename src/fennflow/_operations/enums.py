from enum import auto

from fennflow._str_enum import StrEnum


class OperationTypeEnum(StrEnum):
    """Enum for operation types."""

    CREATE = auto()
    PUT = auto()
    GET = auto()
    DELETE = auto()


class OperationStatusEnum(StrEnum):
    """Enum for operation status."""

    PENDING = auto()
    UPLOADED = auto()
    FAILED = auto()
    COMPENSATION_FAILED = auto()
    DELETED = auto()
