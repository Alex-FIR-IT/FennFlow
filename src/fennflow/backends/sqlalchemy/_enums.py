from fennflow._str_enum import StrEnum


class Dialect(StrEnum):
    POSTGRES = "postgresql"
    SQLITE = "sqlite"


class OutboxStatus(StrEnum):
    CREATED = "created"
    PENDING = "pending"
    FAILED = "failed"
    SENT = "sent"
