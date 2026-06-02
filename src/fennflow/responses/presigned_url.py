from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(slots=True)
class PresignedUrlResponse:
    """Response object returned by presigned URL generation."""

    results: list[str | None]
    """The presigned URL strings or None corresponding to the given paths."""

    @property
    def urls(self) -> Iterator[str]:
        """Iterator that yields presigned URL strings excluding Nones."""
        return filter(None, self.results)

    @property
    def any_url(self) -> bool:
        return any(self.results)
