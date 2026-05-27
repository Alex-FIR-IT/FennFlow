from dataclasses import dataclass


@dataclass(slots=True)
class PresignedUrlResponse:
    """Response object returned by presigned URL generation."""

    url: str
    """The presigned URL string."""
