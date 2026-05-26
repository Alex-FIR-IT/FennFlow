from __future__ import annotations

import json
from pathlib import Path

import pytest

from fennflow.files import MediaType
from fennflow.files.media.binary_content import BinaryContent


class TestBinaryContentFromLocalPath:
    """Tests for BinaryContent.from_local_path."""

    # --- return type is always BinaryContent ---

    def test_returns_binary_content_instance(self, tmp_path: Path):
        f = tmp_path / "file.bin"
        f.write_bytes(b"\x00\x01")
        result = BinaryContent.from_local_path(f)
        assert type(result) is BinaryContent

    def test_txt_file_still_returns_binary_content_not_text_content(
        self, tmp_path: Path
    ):
        # Unlike ContentFactory.from_local_path, this always returns cls,
        # never a subtype resolved from the registry.
        f = tmp_path / "note.txt"
        f.write_bytes(b"hello")
        result = BinaryContent.from_local_path(f)
        assert type(result) is BinaryContent

    # --- MIME type guessing from filename ---

    def test_media_type_guessed_from_txt_extension(self, tmp_path: Path):
        f = tmp_path / "readme.txt"
        f.write_bytes(b"hello")
        result = BinaryContent.from_local_path(f)
        assert result.media_type == MediaType.TEXT_PLAIN

    def test_media_type_guessed_from_png_extension(self, tmp_path: Path):
        f = tmp_path / "image.png"
        f.write_bytes(b"\x89PNG")
        result = BinaryContent.from_local_path(f)
        assert result.media_type == MediaType.IMAGE_PNG

    def test_media_type_guessed_from_json_extension(self, tmp_path: Path):
        f = tmp_path / "data.json"
        f.write_bytes(json.dumps({"k": "v"}).encode())
        result = BinaryContent.from_local_path(f)
        assert result.media_type == MediaType.APPLICATION_JSON

    # --- explicit media_type overrides guessed one ---

    def test_explicit_media_type_overrides_guessed(self, tmp_path: Path):
        f = tmp_path / "data.txt"
        f.write_bytes(b"content")
        result = BinaryContent.from_local_path(
            f, media_type=MediaType.APPLICATION_OCTET_STREAM
        )
        assert result.media_type == MediaType.APPLICATION_OCTET_STREAM

    # --- filename handling ---

    def test_filename_set_from_path_by_default(self, tmp_path: Path):
        f = tmp_path / "myfile.txt"
        f.write_bytes(b"hello")
        result = BinaryContent.from_local_path(f)
        assert result.filename == "myfile.txt"

    def test_explicit_filename_kwarg_overrides_path_name(self, tmp_path: Path):
        f = tmp_path / "original.txt"
        f.write_bytes(b"hello")
        result = BinaryContent.from_local_path(f, filename="renamed.txt")
        assert result.filename == "renamed.txt"

    # --- data correctness ---

    def test_data_matches_file_contents(self, tmp_path: Path):
        raw = b"exact binary content"
        f = tmp_path / "file.bin"
        f.write_bytes(raw)
        result = BinaryContent.from_local_path(f, filename="file.bin")
        assert result.data == raw

    def test_empty_file_produces_empty_bytes(self, tmp_path: Path):
        f = tmp_path / "empty.bin"
        f.write_bytes(b"")
        result = BinaryContent.from_local_path(f, filename="empty.bin")
        assert result.data == b""

    # --- path type acceptance ---

    def test_accepts_string_path(self, tmp_path: Path):
        f = tmp_path / "str.txt"
        f.write_bytes(b"data")
        result = BinaryContent.from_local_path(str(f))
        assert result.data == b"data"

    def test_accepts_pathlib_path(self, tmp_path: Path):
        f = tmp_path / "pathlib.txt"
        f.write_bytes(b"pathlib")
        result = BinaryContent.from_local_path(Path(f))
        assert result.data == b"pathlib"

    # --- extra kwargs ---

    def test_extra_kwargs_forwarded_as_extra_metadata(self, tmp_path: Path):
        f = tmp_path / "meta.txt"
        f.write_bytes(b"x")
        result = BinaryContent.from_local_path(f, custom_tag="abc")
        assert result.extra_metadata.get("custom_tag") == "abc"

    # --- error cases ---

    def test_raises_on_nonexistent_path(self, tmp_path: Path):
        with pytest.raises((FileNotFoundError, OSError)):
            BinaryContent.from_local_path(tmp_path / "ghost.bin")
