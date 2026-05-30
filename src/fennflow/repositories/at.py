from __future__ import annotations

from typing import TYPE_CHECKING

from fennflow._path import Path
from fennflow.path_template import PathTemplate

from .base import BaseRepository

if TYPE_CHECKING:
    from typing_extensions import Self

    from fennflow._new_types import StoragePath


class AtRepository(BaseRepository):
    """Repository mixin that adds path navigation capabilities.

    Allows scoping operations to a specific path within the namespace
    using the ``at()`` method.

    """

    def _join_path(self, *paths: str) -> StoragePath:
        """Join the current path with one or more path segments.

        Args:
            *paths: Path segments to append to the current path.

        Returns:
            The joined and normalized path string.
        """
        return Path.join_path(self._path, *paths)

    def at(self, path: str | PathTemplate) -> Self:
        """Return a new repository instance scoped to the given path.

        Args:
            path: Path to scope the repository to, relative to the current path.

        Returns:
            A new repository instance with the updated path.

        Example::

            storage = uow.user_files.at("user1/")
            print(storage.cwd) # "user1/"

        Example::

            @dataclass(slots=True)
            class YearMonth:
                year: int
                month: int

                def render(self) -> str:
                    return f"{self.year}/{self.month:02d}"

            storage = uow.user_files.at("user1/").at(YearMonth(year=2026, month=1))
            print(storage.cwd) # user1/2026/01/

        """
        if isinstance(path, str):
            resolved = path
        elif isinstance(path, PathTemplate):
            resolved = path.render()
        else:
            raise TypeError(
                f"at() expects a str or PathTemplate, got {type(path).__name__!r}. "
                "Define a render() -> str method on your class "
                "to use it as a path template."
            )

        new_path = self._join_path(resolved)

        return self.__class__(self._uow, new_path, repo_extra=self.repo_extra)

    def _cd_root(self) -> Self:
        """Return a new repository instance scoped to the root path."""
        return self.__class__(
            self._uow,
            "",
            repo_extra=self.repo_extra,
        )

    @property
    def cwd(self) -> str:
        """Return the current working path.

        Returns:
            The normalized current path string.
        """
        return Path.normalize_folder(self._path)
