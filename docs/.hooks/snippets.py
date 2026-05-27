import re
from pathlib import Path


def on_page_read_source(page, config):
    src_path = Path(page.file.abs_src_path)
    content = src_path.read_text(encoding="utf-8")

    def replace(match):
        file_path = Path(match.group(1))
        if not file_path.is_absolute():
            file_path = Path(config["docs_dir"]).parent / file_path
        return file_path.read_text(encoding="utf-8").rstrip()

    return re.sub(
        r'```python file="([^"]+)"(.*?)```',
        lambda m: f"```python\n{replace(m)}\n```",
        content,
        flags=re.DOTALL,
    )
