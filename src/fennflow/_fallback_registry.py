from collections.abc import Callable, Mapping
from typing import Generic, TypeVar

from fennflow._sentinel import OMIT, Omittable, is_given

Key = TypeVar("Key")
Value = TypeVar("Value")
DefaultValue = TypeVar("DefaultValue")


class FallbackRegistry(Generic[Key, Value, DefaultValue]):
    def __init__(
        self,
        registry: Mapping[Key, Value],
        default_value: Omittable[DefaultValue] = OMIT,
        default_factory: Omittable[Callable[[], DefaultValue]] = OMIT,
    ):
        if is_given(default_value) and is_given(default_factory):
            raise ValueError("cannot specify both default and default_factory")

        self._registry = registry
        self._default_value = default_value
        self._default_factory = default_factory

    def __getitem__(self, key: Key) -> Value | DefaultValue:
        try:
            return self._registry[key]
        except KeyError:
            if is_given(self._default_factory):
                return self._default_factory()

            if is_given(self._default_value):
                return self._default_value

            raise
