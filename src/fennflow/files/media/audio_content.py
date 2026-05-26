from .base_binary import BaseBinary


class AudioContent(BaseBinary):
    """Media content representing an audio file.

    Attributes:
        duration: Duration of the audio in seconds, if known.
    """

    duration: int | None = None
