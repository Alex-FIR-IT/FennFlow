from typing import TypeVar

from fennflow._query_specs.base import BaseQuerySpec

ReturnType_co = TypeVar(
    "ReturnType_co",
    covariant=True,
)

QuerySpecT_contra = TypeVar(
    "QuerySpecT_contra",
    bound=BaseQuerySpec,
    contravariant=True,
)
