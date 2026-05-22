from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fennflow._query_specs.select.base import SelectQuerySpec
from fennflow._sentinel import OMIT, Omittable
from fennflow.backends.responses import RecordPage

if TYPE_CHECKING:
    from uuid import UUID

    from fennflow._new_types import BackendScope, Namespace


@dataclass(slots=True, frozen=True)
class SelectVisibleQuerySpec(SelectQuerySpec[RecordPage]):
    """Select records visible to the current session.

    SELECT
        <record fields>
    FROM
        <table>
    WHERE
        scope = <scope>
        AND namespace = <namespace>
        AND storage_path LIKE <prefix || '%'>
        AND (
            status = 'uploaded'
            OR (
                status = 'pending'
                AND session_id = <session_id>
                AND operation_type IN (<inserting_types>)
            )
        )
        AND (
            <continuation_token> IS NULL
            OR storage_path < <continuation_token>
        )
    ORDER BY
        storage_path DESC
    LIMIT
        <limit>
    """

    scope: BackendScope
    namespace: Namespace
    prefix: str
    limit: int
    session_id: UUID
    continuation_token: Omittable[str] = OMIT
