from typing import Literal

from fennflow._base_pydantic_config import BasePydanticConfig
from fennflow.reconciler.enums import ReconcileFrequencyEnum, ReconcileStrategyEnum


class ReconcileConfig(BasePydanticConfig):
    """Configuration for the reconciler."""

    frequency: (
        Literal["on_start_app", "on_session_start", "never"] | ReconcileFrequencyEnum
    ) = ReconcileFrequencyEnum.ON_START_APP
    strategy: (
        Literal["fill_if_empty", "replace", "insert_missing"] | ReconcileStrategyEnum
    ) = ReconcileStrategyEnum.FILL_IF_EMPTY
    batch_size: int = 1000
