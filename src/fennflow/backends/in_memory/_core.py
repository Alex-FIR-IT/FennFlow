from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from fennflow.backends._abstract.core import AbstractBackend

if TYPE_CHECKING:
    from typing_extensions import Self

    from fennflow._query_specs.base import BaseQuerySpec
    from fennflow._query_specs.dispatcher import Dispatcher
    from fennflow.backends import InMemoryBackendConfig
    from fennflow.backends.in_memory._types import (
        InMemoryStorageType,
        ScopedStorageType,
    )

ReturnType = TypeVar("ReturnType")


class InMemoryBackend(AbstractBackend):
    _instance: ClassVar[Self | None] = None
    _initialized: ClassVar[bool] = False

    def __new__(cls, *args, **kwargs):  # noqa: ARG004

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(
        self,
        dispatcher: Dispatcher,
        storage: InMemoryStorageType,
        config: InMemoryBackendConfig,
    ) -> None:
        if self.__class__._initialized:
            return

        self.storage = storage
        self.dispatcher = dispatcher
        self._config = config

        self.__class__._initialized = True

    @property
    def scoped_storage(self) -> ScopedStorageType:
        return self.storage[self._config.scope]

    async def execute(self, query: BaseQuerySpec[ReturnType]) -> ReturnType:
        return await self.dispatcher.dispatch(query_spec=query)

    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def open(self) -> None:
        pass

    async def close(self) -> None:
        pass

    def clear(self):
        self.scoped_storage.clear()
