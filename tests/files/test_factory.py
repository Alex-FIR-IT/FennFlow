from __future__ import annotations

import json
from pathlib import Path

import pytest

from fennflow.files import MediaType
from fennflow.files.exceptions import ExtensionCannotBeGuessed
from fennflow.files.factory import ContentFactory
from fennflow.files.media.audio_content import AudioContent
from fennflow.files.media.binary_content import BinaryContent
from fennflow.files.media.image_content import ImageContent
from fennflow.files.media.json_content import JsonContent
from fennflow.files.media.text_content import TextContent
from fennflow.files.media.url_content import UrlContent
from fennflow.files.media.video_content import VideoContent

# ---------------------------------------------------------------------------
# ContentFactory.from_bytes
# ---------------------------------------------------------------------------


class TestFromBytes:
    """Tests for ContentFactory.from_bytes."""

    # --- correct type resolution ---

    def test_text_plain_returns_text_content(self):
        result = ContentFactory.from_bytes(MediaType.TEXT_PLAIN, b"hello")
        assert isinstance(result, TextContent)

    def test_application_json_returns_json_content(self):
        result = ContentFactory.from_bytes(
            MediaType.APPLICATION_JSON, json.dumps({"k": "v"}).encode()
        )
        assert isinstance(result, JsonContent)

    def test_image_png_returns_image_content(self):
        result = ContentFactory.from_bytes(MediaType.IMAGE_PNG, b"\x89PNG")
        assert isinstance(result, ImageContent)

    def test_image_jpeg_returns_image_content(self):
        result = ContentFactory.from_bytes(MediaType.IMAGE_JPEG, b"\xff\xd8\xff")
        assert isinstance(result, ImageContent)

    def test_audio_mpeg_returns_audio_content(self):
        result = ContentFactory.from_bytes(MediaType.AUDIO_MPEG, b"\xff\xfb")
        assert isinstance(result, AudioContent)

    def test_video_mp4_returns_video_content(self):
        result = ContentFactory.from_bytes(MediaType.VIDEO_MP4, b"\x00\x00\x00\x18")
        assert isinstance(result, VideoContent)

    def test_unknown_mime_type_falls_and_raises(self):
        with pytest.raises(ExtensionCannotBeGuessed):
            ContentFactory.from_bytes("application/x-totally-made-up", b"\x00\x01\x02")

    def test_unknown_mime_type_with_filename_not_raises(self):
        filename = "some.txt"

        result = ContentFactory.from_bytes(
            "application/x-totally-made-up",
            b"\x00\x01\x02",
            filename=filename,
        )

        assert type(result) is BinaryContent
        assert result.filename == filename

    def test_prefix_match_resolves_image_subtype(self):
        # IMAGE_WEBP — not registered by exact key, "image/" prefix should match
        result = ContentFactory.from_bytes(MediaType.IMAGE_WEBP, b"RIFF")
        assert isinstance(result, ImageContent)

    def test_prefix_match_resolves_audio_subtype(self):
        result = ContentFactory.from_bytes(MediaType.AUDIO_OGG, b"OggS")
        assert isinstance(result, AudioContent)

    # --- data round-trip ---

    def test_data_is_preserved(self):
        raw = b"some raw bytes"
        result = ContentFactory.from_bytes(MediaType.APPLICATION_OCTET_STREAM, raw)
        assert result.data == raw

    def test_text_content_property_decoded(self):
        text = "Hello, FennFlow!"
        result = ContentFactory.from_bytes(MediaType.TEXT_PLAIN, text.encode())
        assert isinstance(result, TextContent)
        assert result.content == text

    def test_json_content_property_parsed(self):
        payload = {"key": "value", "num": 42}
        result = ContentFactory.from_bytes(
            MediaType.APPLICATION_JSON, json.dumps(payload).encode()
        )
        assert isinstance(result, JsonContent)
        assert result.content == payload

    # --- kwargs forwarding ---

    def test_extra_kwargs_stored_as_extra_metadata(self):
        result = ContentFactory.from_bytes(
            MediaType.TEXT_PLAIN, b"hi", custom_field="my_value"
        )
        assert result.extra_metadata.get("custom_field") == "my_value"

    def test_explicit_filename_kwarg_is_accepted(self):
        result = ContentFactory.from_bytes(
            MediaType.TEXT_PLAIN, b"hello", filename="readme.txt"
        )
        assert result.filename == "readme.txt"

    # --- media_type stored on result ---

    def test_media_type_is_set_on_result(self):
        result = ContentFactory.from_bytes(MediaType.TEXT_PLAIN, b"text")
        assert result.media_type == MediaType.TEXT_PLAIN


# ---------------------------------------------------------------------------
# ContentFactory.from_url
# ---------------------------------------------------------------------------


class TestFromUrl:
    """Tests for ContentFactory.from_url."""

    def test_returns_url_content(self):
        result = ContentFactory.from_url("https://example.com/file.txt")
        assert isinstance(result, UrlContent)
        assert result.filename == "file.txt"

    def test_data_is_url_string(self):
        url = "https://example.com/file.txt"
        result = ContentFactory.from_url(url)
        assert result.data == url

    def test_default_media_type_is_octet_stream(self):
        result = ContentFactory.from_url("https://example.com/blob")
        assert result.media_type == MediaType.APPLICATION_OCTET_STREAM

    def test_custom_media_type_is_stored(self):
        result = ContentFactory.from_url(
            "https://example.com/img.png", media_type=MediaType.IMAGE_PNG
        )
        assert result.media_type == MediaType.IMAGE_PNG

    def test_filename_auto_generated_when_not_provided(self):
        # Implementation calls FilenameGenerator.generate_from_string(url)
        # when filename is absent — we only assert it is truthy, not its exact value
        # since the generation algorithm is an internal concern.
        result = ContentFactory.from_url("https://example.com/blob")
        assert result.filename  # non-empty, non-None

    def test_explicit_filename_overrides_generated_one(self):
        result = ContentFactory.from_url(
            "https://example.com/blob", filename="override.bin"
        )
        assert result.filename == "override.bin"

    def test_extra_kwargs_are_forwarded(self):
        result = ContentFactory.from_url(
            "https://example.com/f.txt",
            media_type=MediaType.TEXT_PLAIN,
            custom_tag="v1",
        )
        assert result.extra_metadata.get("custom_tag") == "v1"


# ---------------------------------------------------------------------------
# ContentFactory.from_local_path
# ---------------------------------------------------------------------------


class TestFromLocalPath:
    """Tests for ContentFactory.from_local_path."""

    # --- return type resolution ---

    def test_txt_file_returns_text_content(self, tmp_path: Path):
        f = tmp_path / "note.txt"
        f.write_bytes(b"hello")
        result = ContentFactory.from_local_path(f)
        assert isinstance(result, TextContent)

    def test_unknown_extension_falls_back_to_binary_content(self, tmp_path: Path):
        f = tmp_path / "sample.bin"
        f.write_bytes(b"\x00\x01\x02\x03")
        result = ContentFactory.from_local_path(f)
        assert isinstance(result, BinaryContent)

    def test_explicit_media_type_overrides_guessed_type(self, tmp_path: Path):
        # File is .txt but we force JSON media type
        f = tmp_path / "data.txt"
        f.write_bytes(json.dumps({"x": 1}).encode())
        result = ContentFactory.from_local_path(
            f,
            media_type=MediaType.APPLICATION_JSON,
        )
        assert isinstance(result, JsonContent)

    # --- data and filename ---

    def test_data_matches_file_contents(self, tmp_path: Path):
        raw = b"exact content"
        f = tmp_path / "file.txt"
        f.write_bytes(raw)
        result = ContentFactory.from_local_path(f)
        assert result.data == raw

    def test_filename_taken_from_path(self, tmp_path: Path):
        f = tmp_path / "myfile.txt"
        f.write_bytes(b"hello")
        result = ContentFactory.from_local_path(f)
        assert result.filename == "myfile.txt"

    def test_explicit_filename_kwarg_overrides_path_name(self, tmp_path: Path):
        f = tmp_path / "original.txt"
        f.write_bytes(b"hello")
        result = ContentFactory.from_local_path(f, filename="renamed.txt")
        assert result.filename == "renamed.txt"

    # --- path type acceptance ---

    def test_accepts_string_path(self, tmp_path: Path):
        f = tmp_path / "str_path.txt"
        f.write_bytes(b"data")
        result = ContentFactory.from_local_path(str(f))
        assert result.data == b"data"

    def test_accepts_pathlib_path(self, tmp_path: Path):
        f = tmp_path / "pathlib.txt"
        f.write_bytes(b"pathlib")
        result = ContentFactory.from_local_path(Path(f))
        assert result.data == b"pathlib"

    # --- edge cases ---

    def test_empty_file_is_read_correctly(self, tmp_path: Path):
        f = tmp_path / "empty.txt"
        f.write_bytes(b"")
        result = ContentFactory.from_local_path(f)
        assert result.data == b""

    def test_extra_kwargs_are_forwarded_as_extra_metadata(self, tmp_path: Path):
        f = tmp_path / "extra.txt"
        f.write_bytes(b"x")
        result = ContentFactory.from_local_path(f, custom_meta="abc")
        assert result.extra_metadata.get("custom_meta") == "abc"

    def test_raises_on_nonexistent_path(self, tmp_path: Path):
        with pytest.raises((FileNotFoundError, OSError)):
            ContentFactory.from_local_path(tmp_path / "does_not_exist.bin")
