from fennflow._str_enum import StrEnum


class Dialect(StrEnum):
    POSTGRES = "postgresql"
    SQLITE = "sqlite"


class OutboxStatus(StrEnum):
    PENDING = "pending"
    FAILED = "failed"
    SENT = "sent"
