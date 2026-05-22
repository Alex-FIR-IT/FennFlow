from dataclasses import dataclass

from fennflow._query_specs.delete.base import DeleteQuerySpec


@dataclass(slots=True, frozen=True)
class DeleteScopeQuerySpec(DeleteQuerySpec[None]):
    """Base class for delete query specifications.

    DELETE FROM
        <table>
    WHERE
        scope = <scope>
    """

    scope: str
