from enum import StrEnum, auto


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
