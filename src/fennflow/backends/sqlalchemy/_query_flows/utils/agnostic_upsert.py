from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from fennflow.backends.sqlalchemy._base import AbstractOperationRecordModel


async def upsert(
    session: AsyncSession,
    orm_instance: AbstractOperationRecordModel,
):
    """An upsert operation.

    Check whether instance with our pk was already inserted in session.
    If we find such an object, then expunge (delete) it from the session and then merge.
    Otherwise, just merge.
    """
    new_orm_instances = {obj.pk: obj for obj in session.new}
    if orm_instance.pk in new_orm_instances:
        session.expunge(new_orm_instances[orm_instance.pk])

    return await session.merge(orm_instance)
