from fennflow._str_enum import StrEnum


class MediaType(StrEnum):
    """Common MIME types for use with FennFlow content models."""

    # --- Text (→ TextContent) ---
    TEXT_PLAIN = "text/plain"
    TEXT_HTML = "text/html"
    TEXT_CSS = "text/css"
    TEXT_CSV = "text/csv"
    TEXT_XML = "text/xml"
    TEXT_MARKDOWN = "text/markdown"

    # --- Application / structured (→ JsonContent or DocumentContent) ---
    APPLICATION_JSON = "application/json"
    APPLICATION_XML = "application/xml"
    APPLICATION_PDF = "application/pdf"
    APPLICATION_ZIP = "application/zip"
    APPLICATION_GZIP = "application/gzip"
    APPLICATION_OCTET_STREAM = "application/octet-stream"

    # --- Images (→ ImageContent) ---
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    IMAGE_GIF = "image/gif"
    IMAGE_WEBP = "image/webp"
    IMAGE_SVG = "image/svg+xml"
    IMAGE_TIFF = "image/tiff"
    IMAGE_BMP = "image/bmp"
    IMAGE_ICO = "image/x-icon"

    # --- Audio (→ AudioContent) ---
    AUDIO_MPEG = "audio/mpeg"
    AUDIO_OGG = "audio/ogg"
    AUDIO_WAV = "audio/wav"
    AUDIO_WEBM = "audio/webm"
    AUDIO_FLAC = "audio/flac"
    AUDIO_AAC = "audio/aac"

    # --- Video (→ VideoContent) ---
    VIDEO_MP4 = "video/mp4"
    VIDEO_WEBM = "video/webm"
    VIDEO_OGG = "video/ogg"
    VIDEO_QUICKTIME = "video/quicktime"
    VIDEO_AVI = "video/x-msvideo"
