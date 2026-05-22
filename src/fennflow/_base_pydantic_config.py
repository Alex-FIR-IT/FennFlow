from pydantic import BaseModel, ConfigDict


class BasePydanticConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
