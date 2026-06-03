from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._sentinel import OMIT, Omittable
from fennflow.repositories import ListRepository

if TYPE_CHECKING:
    from fennflow._new_types import StoragePath
    from fennflow._protocols.repository import RepositoryProtocol


async def get_all_paths(
    repository: RepositoryProtocol,
    prefix: str,
) -> list[StoragePath]:
    continue_flag = True
    continuation_token: Omittable[str] = OMIT
    paths: list[str] = []
    list_repository = ListRepository(
        uow=repository._uow,
        path=repository._path,
        repo_extra=repository.repo_extra,
    )

    while continue_flag:
        list_response = await list_repository.list(
            prefix=prefix,
            continuation_token=continuation_token,
        )
        paths.extend(list_response)
        continuation_token = list_response.continuation_token or OMIT

        continue_flag = bool(list_response.continuation_token)

    return paths
