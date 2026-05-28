from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fennflow._new_types import BackendScope, Namespace

NAMESPACE: Namespace = "user-files"
SCOPE: BackendScope = "default"

try:
    PYTEST_USE_MINIO = bool(int(os.getenv("PYTEST_USE_MINIO", "0")))
except ValueError as _type_error:
    raise ValueError("PYTEST_USE_MINIO takes either 0 or 1") from _type_error
