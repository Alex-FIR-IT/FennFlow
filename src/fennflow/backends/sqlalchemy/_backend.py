from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from fennflow._query_specs.dispatcher import Dispatcher
from fennflow.backends._abstract.core import AbstractBackend

from ._adapter import RecordOrmAdapter
from ._engine import async_engine_factory
from ._model import create_all, create_operation_record_model

if TYPE_CHECKING:
    from fennflow.backends.sqlalchemy.config import SqlalchemyBackendConfig

    from ..._query_specs.base import BaseQuerySpec
    from ._base import AsyncSession

ReturnType = TypeVar("ReturnType")


class SqlalchemyBackend(AbstractBackend):
    def __init__(
        self,
        config: SqlalchemyBackendConfig,
    ) -> None:
        from ._base import async_sessionmaker

        self._session: AsyncSession | None = None
        self._dispatcher: Dispatcher | None = None
        self._config = config
        self._engine = async_engine_factory(
            url=self._config.database_url,
            schema=self._config.db_schema,
        )

        self._orm_model = create_operation_record_model(
            table_name=config.scope,
            schema=config.db_schema,
            dialect=self._engine.dialect.name,
        )
        self._adapter = RecordOrmAdapter(orm_model=self._orm_model)

        self._session_maker = async_sessionmaker(
            self._engine,
        )

    async def execute(
        self,
        query: BaseQuerySpec[ReturnType],
    ) -> ReturnType:
        return await self.dispatcher.dispatch(query_spec=query)

    @property
    def session(
        self,
    ) -> AsyncSession:
        if self._session is None:
            raise RuntimeError("Session is not set. Call open() method.")

        return self._session

    @property
    def dispatcher(
        self,
    ) -> Dispatcher:
        if self._dispatcher is None:
            raise RuntimeError("Dispatcher is not set. Call open() method.")

        return self._dispatcher

    async def commit(
        self,
    ):
        await self.session.commit()

    async def rollback(
        self,
    ):
        await self.session.rollback()

    async def open(
        self,
    ) -> None:
        from ._factory import SqlalchemyBackendFactory

        await create_all(
            engine=self._engine,
            schema=self._config.db_schema,
        )
        self._session = self._session_maker()
        self._dispatcher = Dispatcher(
            registry=SqlalchemyBackendFactory._create_registry(
                config=self._config,
                session=self.session,
                adapter=self._adapter,
                dialect=self._engine.dialect.name,
            ),
        )

    async def close(
        self,
    ) -> None:
        if self._session is not None:
            await self._session.close()
        self._session = None
        self._dispatcher = None
