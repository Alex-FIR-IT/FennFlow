from pydantic import BaseModel, Field

from fennflow._base_pydantic_config import BasePydanticConfig


class AbstractConnectorConfig(BasePydanticConfig):
    """Abstract configuration for all FennFlow connectors."""

    scope: BackendScope = Field(
        default="default_scope",
        description="Label to isolate backend state. "
        "Useful when working with multiple storage instances "
        "(e.g. two S3 or S3 and MinIO) "
        "to avoid merging their files' metadata.",
    )
