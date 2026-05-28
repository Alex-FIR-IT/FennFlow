"""
Used to check that examples are at least valid syntax
and can be imported without errors.

"""

from pathlib import Path

import pytest

from examples.path_templates import main as path_template_main
from examples.testing import db, test_register_user_saves_avatar


@pytest.mark.asyncio
async def test_path_template():
    await path_template_main()


@pytest.mark.asyncio
async def test_base_upload_import():
    examples_dir = Path(__file__).parent.parent / "examples"
    assert examples_dir.is_dir(), f"No examples directory found at {examples_dir}"
    count = 0
    for example in examples_dir.glob("*.py"):
        print(f"Importing {example.stem}...")
        __import__(f"examples.{example.stem}")
        count += 1

    print(f"Imported {count} examples")
    assert count > 5, "No examples found"
