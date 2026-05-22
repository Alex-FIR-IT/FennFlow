from dataclasses import dataclass

from fennflow._new_types import BackendScope
from fennflow._query_specs.select.base import SelectQuerySpec


@dataclass(slots=True, frozen=True)
class IsEmptyQuerySpec(SelectQuerySpec[bool]):
    """Check if there are no records in current scope.

    SELECT NOT EXISTS (
        SELECT
            1
        FROM
            <table>
        WHERE
            scope = <scope>
    ) AS is_empty
    """

    scope: BackendScope
