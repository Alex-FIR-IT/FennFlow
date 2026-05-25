from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._path import Path

if TYPE_CHECKING:
    from fennflow._new_types import StoragePath
    from fennflow._operations.dto import Record


class TmpPathBuilder:
    @staticmethod
    def from_record(record: Record) -> StoragePath:
        return Path.join_path(
            "fennflow",
            "tmp",
            f"session_id_{record.session_id}",
            f"operation_id_{record.operation_id}",
            record.storage_path,
        )
