from dataclasses import dataclass

from fennflow._base_pydantic_config import BasePydanticConfig
from fennflow.reconciler.enums import ReconcileFrequencyEnum, ReconcileStrategyEnum


class ReconcileConfig(BasePydanticConfig):
    """Configuration for the reconciler."""

    frequency: ReconcileFrequencyEnum = ReconcileFrequencyEnum.ON_START_APP
    strategy: ReconcileStrategyEnum = ReconcileStrategyEnum.FILL_IF_EMPTY
    batch_size: int = 1000
