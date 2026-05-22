from fennflow import UnitOfWork
from fennflow._new_types import BackendScope
from fennflow._query_specs.delete.delete_scope import DeleteScopeQuerySpec
from fennflow.connectors import InMemoryConnector
from fennflow.reconciler._orchestrator import ReconcileOrchestrator


async def reset_state(
    uow_cls: type[UnitOfWork],
    scope: BackendScope,
) -> None:
    async with uow_cls() as uow:
        await uow._backend.backend_engine.execute(DeleteScopeQuerySpec(scope=scope))

    InMemoryConnector.drop_all()
    ReconcileOrchestrator._reconciled_on_startup = set()
