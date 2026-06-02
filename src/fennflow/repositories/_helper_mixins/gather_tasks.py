import asyncio
from collections.abc import Coroutine
from typing import Any, TypeVar

T = TypeVar("T")


class GatherTasksHelper:
    @staticmethod
    async def _gather_tasks(
        tasks: list[Coroutine[Any, Any, T]],
        task_indexes: list[int],
        results: list[None | T],
    ) -> list[None | T]:
        gathered = await asyncio.gather(*tasks)
        for i, result in zip(task_indexes, gathered, strict=True):
            results[i] = result
        return results
