from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fennflow._operations.dto import Record
from fennflow._query_specs.select.base import SelectQuerySpec

if TYPE_CHECKING:
    from uuid import UUID

    from fennflow._new_types import BackendScope, Namespace, StoragePath


@dataclass(slots=True, frozen=True)
class GetVisibleQuerySpec(SelectQuerySpec[Record | None]):
    """Select one concrete record visible to the current session.

    SELECT
        <record fields>
    FROM
        <table>
    WHERE
        scope = <scope>
        AND namespace = <namespace>
        AND storage_path = <storage_path>
        AND (
                status = 'uploaded'
                OR (
                    status = 'pending'
                    AND session_id = <session_id>
                    AND operation_type IN (<inserting_types>)
                    )
            )
    LIMIT
        1
    """

    scope: BackendScope
    namespace: Namespace
    storage_path: StoragePath
    session_id: UUID
