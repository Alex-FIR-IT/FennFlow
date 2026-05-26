from .base_binary import BaseBinary


class ImageContent(BaseBinary):
    """Media content representing an image file.

    Attributes:
        height: Height of the image in pixels, if known.
        width: Width of the image in pixels, if known.
    """

    height: int | None = None
    width: int | None = None
