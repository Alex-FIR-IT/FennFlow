from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from uuid import UUID

    from typing_extensions import NotRequired

    from fennflow._new_types import Namespace, StoragePath
    from fennflow._operations.enums import OperationStatusEnum
    from fennflow._sentinel import Omittable
    from fennflow.files._annotations import MediaTypes


class SelectParams(TypedDict):
    """TypedDict describes arguments for select operation.

    For now, it exists only in InMemoryBackend.
    """

    path: NotRequired[StoragePath]
    prefix: NotRequired[str]
    namespace: NotRequired[Namespace]
    status: NotRequired[OperationStatusEnum]
    media_type: NotRequired[MediaTypes]
    session_id: NotRequired[UUID]
    operation_id: NotRequired[UUID]
    is_expired: NotRequired[bool]
    limit: NotRequired[int]
    continuation_token: Omittable[str]
    visible_for_session_id: NotRequired[UUID]
