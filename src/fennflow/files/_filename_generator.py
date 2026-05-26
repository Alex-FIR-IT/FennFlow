from hashlib import sha256
from pathlib import Path


class FilenameGenerator:
    """Class for generating filenames."""

    @staticmethod
    def generate_from_bytes(bytes_content: bytes | bytearray) -> str:
        return sha256(bytes_content).hexdigest()

    @classmethod
    def generate_from_string(
        cls,
        string_content: str,
        encoding: str = "utf-8",
    ) -> str:
        return cls.generate_from_bytes(string_content.encode(encoding))

    @classmethod
    def generate_from_url(
        cls,
        url: str,
        encoding: str = "utf-8",
    ) -> str:
        path = Path(url)

        if path.suffix:
            return path.name
        else:
            string_content = url

        return cls.generate_from_bytes(string_content.encode(encoding))
