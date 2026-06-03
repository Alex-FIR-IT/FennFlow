"""Tests for GetPrefixRepository."""

import pytest

from fennflow.files import JsonContent, MediaType, TextContent
from fennflow.files.media.binary_content import BinaryContent


async def _seed(prefix: str, *files, uow_cls):
    """Upload files and commit so they're visible to new sessions."""
    async with uow_cls() as uow:
        await uow.user_files.at(prefix).put(*files)


@pytest.mark.asyncio
async def test_get_prefix_returns_files_under_prefix(uow_cls):
    txt = TextContent.from_content("hello")
    jsn = JsonContent.from_content({"key": "value"})
    await _seed(
        "docs/",
        txt,
        jsn,
        uow_cls=uow_cls,
    )

    async with uow_cls() as uow:
        response = await uow.user_files.get_prefix("docs/")

    assert len(response) == 2


@pytest.mark.asyncio
async def test_get_prefix_empty_prefix_returns_all_files(uow_cls):
    txt = TextContent.from_content("a")
    jsn = JsonContent.from_content([1, 2])
    await _seed(
        "folder/",
        txt,
        jsn,
        uow_cls=uow_cls,
    )

    async with uow_cls() as uow:
        response = await uow.user_files.get_prefix("")

    assert len(response) == 2


@pytest.mark.asyncio
async def test_get_prefix_returns_empty_response_when_nothing_matches(uow_cls):
    txt = TextContent.from_content("irrelevant")
    await _seed(
        "images/",
        txt,
        uow_cls=uow_cls,
    )

    async with uow_cls() as uow:
        response = await uow.user_files.get_prefix("docs/")

    assert len(response) == 0
    assert not response  # MediaResponse is falsy when empty


@pytest.mark.asyncio
async def test_get_prefix_does_not_return_files_outside_prefix(uow_cls):
    docs_file = TextContent.from_content("in docs")
    images_file = BinaryContent(
        data=b"\x89PNG", media_type=MediaType.IMAGE_PNG, filename="img.png"
    )
    await _seed(
        "docs/",
        docs_file,
        uow_cls=uow_cls,
    )
    await _seed(
        "images/",
        images_file,
        uow_cls=uow_cls,
    )

    async with uow_cls() as uow:
        response = await uow.user_files.get_prefix("docs/")

    assert len(response) == 1
    assert response.texts[0].content.content == "in docs"


@pytest.mark.asyncio
async def test_get_prefix_scoped_via_at_is_additive(uow_cls):
    """at() + get_prefix() should combine paths."""
    file_a = TextContent.from_content("a")
    file_b = TextContent.from_content("b")
    await _seed(
        "user1/reports/",
        file_a,
        file_b,
        uow_cls=uow_cls,
    )

    # should not see them
    await _seed(
        "user2/reports/",
        TextContent.from_content("other"),
        uow_cls=uow_cls,
    )

    async with uow_cls() as uow:
        response = await uow.user_files.at("user1/").get_prefix("reports/")

    assert len(response) == 2


# ---------------------------------------------------------------------------
# Large result sets (pagination path)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_prefix_retrieves_all_files_across_pages(uow_cls):
    """get_prefix should collect all pages, not just the first batch."""
    files = [
        TextContent.from_content(f"content-{i}", filename=f"file_{i:04d}.txt")
        for i in range(1050)
    ]
    await _seed("bulk/", *files, uow_cls=uow_cls)

    async with uow_cls() as uow:
        response = await uow.user_files.get_prefix("bulk/")

    assert len(response) == 1050
