from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from fennflow import UnitOfWork
    from fennflow.repositories.fields.base import RepoExtra


class RepositoryProtocol(Protocol):
    _uow: UnitOfWork
    _path: str
    repo_extra: RepoExtra
