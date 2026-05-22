from dataclasses import dataclass

from fennflow._new_types import BackendScope, Namespace, StoragePath
from fennflow._operations.dto import Record
from fennflow._query_specs.select.base import SelectQuerySpec


@dataclass(slots=True, frozen=True)
class GetByStoragePathQuerySpec(SelectQuerySpec[Record | None]):
    """Select one record by the storage path.

    SELECT
        <record fields>
    FROM
        <table>
    WHERE
        scope = <scope>
        AND namespace = <namespace>
        AND storage_path = <storage_path>
    LIMIT
        1

    """

    scope: BackendScope
    namespace: Namespace
    storage_path: StoragePath
