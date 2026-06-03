"""Tests for GeneratePresignedUrlPrefixRepository."""

import pytest

from fennflow.files import JsonContent, MediaType, TextContent
from fennflow.files.media.binary_content import BinaryContent


async def _seed(prefix: str, *files, uow_cls):
    """Upload files and commit so they're visible to new sessions."""
    async with uow_cls() as uow:
        await uow.user_files.at(prefix).put(*files)


@pytest.mark.asyncio
async def test_generate_presigned_url_prefix_returns_urls_under_prefix(uow_cls):
    txt = TextContent.from_content("hello")
    jsn = JsonContent.from_content({"key": "value"})
    await _seed("docs/", txt, jsn, uow_cls=uow_cls)

    async with uow_cls() as uow:
        response = await uow.user_files.generate_presigned_url_prefix("docs/")

    assert len(list(response.urls)) == 2


@pytest.mark.asyncio
async def test_generate_presigned_url_prefix_empty_prefix_returns_all(uow_cls):
    txt = TextContent.from_content("a")
    jsn = JsonContent.from_content([1, 2])
    await _seed("folder/", txt, jsn, uow_cls=uow_cls)

    async with uow_cls() as uow:
        response = await uow.user_files.generate_presigned_url_prefix("")

    assert len(list(response.urls)) == 2


@pytest.mark.asyncio
async def test_generate_presigned_url_prefix_returns_empty_when_nothing_matches(
    uow_cls,
):
    txt = TextContent.from_content("irrelevant")
    await _seed("images/", txt, uow_cls=uow_cls)

    async with uow_cls() as uow:
        response = await uow.user_files.generate_presigned_url_prefix("docs/")

    assert len(list(response.urls)) == 0


@pytest.mark.asyncio
async def test_generate_presigned_url_prefix_does_not_return_files_outside_prefix(
    uow_cls,
):
    docs_file = TextContent.from_content("in docs")
    images_file = BinaryContent(
        data=b"\x89PNG", media_type=MediaType.IMAGE_PNG, filename="img.png"
    )
    await _seed("docs/", docs_file, uow_cls=uow_cls)
    await _seed("images/", images_file, uow_cls=uow_cls)

    async with uow_cls() as uow:
        response = await uow.user_files.generate_presigned_url_prefix("docs/")

    urls = list(response.urls)
    assert len(urls) == 1


@pytest.mark.asyncio
async def test_generate_presigned_url_prefix_scoped_via_at_is_additive(uow_cls):
    """at() + generate_presigned_url_prefix() should combine paths."""
    file_a = TextContent.from_content("a")
    file_b = TextContent.from_content("b")
    await _seed("user1/reports/", file_a, file_b, uow_cls=uow_cls)

    await _seed("user2/reports/", TextContent.from_content("other"), uow_cls=uow_cls)

    async with uow_cls() as uow:
        response = await uow.user_files.at("user1/").generate_presigned_url_prefix(
            "reports/"
        )

    assert len(list(response.urls)) == 2


@pytest.mark.asyncio
async def test_generate_presigned_url_prefix_results_length_matches_files(uow_cls):
    """response.results should have one entry per file found under prefix."""
    file_a = TextContent.from_content("x")
    file_b = TextContent.from_content("y")
    await _seed("data/", file_a, file_b, uow_cls=uow_cls)

    async with uow_cls() as uow:
        response = await uow.user_files.generate_presigned_url_prefix("data/")

    assert len(response.results) == len(tuple(response.urls)) == 2


@pytest.mark.asyncio
async def test_generate_presigned_url_prefix_retrieves_all_files_across_pages(uow_cls):
    """generate_presigned_url_prefix should collect all pages."""
    files = [
        TextContent.from_content(f"content-{i}", filename=f"file_{i:04d}.txt")
        for i in range(1050)
    ]
    await _seed("bulk/", *files, uow_cls=uow_cls)

    async with uow_cls() as uow:
        response = await uow.user_files.generate_presigned_url_prefix("bulk/")

    assert len(list(response.urls)) == 1050
