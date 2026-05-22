from __future__ import annotations

from dataclasses import dataclass

from fennflow._query_specs.select.base import SelectQuerySpec


@dataclass(slots=True, frozen=True)
class CountQuerySpec(SelectQuerySpec[int]):
    """Select count of records.

    SELECT
        COUNT(*)
    FROM
        <table>
    """
