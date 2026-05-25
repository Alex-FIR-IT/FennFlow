from pydantic import Field

from fennflow._base_pydantic_config import BasePydanticConfig
from fennflow._new_types import BackendScope


class AbstractBackendConfig(BasePydanticConfig):
    """Base configuration for all FennFlow backends."""

    scope: BackendScope = Field(
        default="default",
        description="Label to isolate backend state. "
        "Useful when working with multiple storage instances "
        "(e.g. two S3 or S3 and MinIO) "
        "to avoid merging their files' metadata.",
    )
