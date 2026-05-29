import pytest

from fennflow.files import (
    DocumentContent,
    ImageContent,
    JsonContent,
    MediaType,
    TextContent,
    VideoContent,
)


@pytest.mark.asyncio
async def test_media_response_properties(uow_cls):
    text_file = TextContent.from_content("Hello, world!")
    json_file = JsonContent.from_content({"user": "alice", "score": 42})
    image_file = ImageContent(media_type=MediaType.IMAGE_PNG, data=b"fjdkfj")
    video_file = VideoContent(media_type=MediaType.VIDEO_AVI, data=b"fkdjf")
    document_file = DocumentContent(media_type=MediaType.APPLICATION_PDF, data=b"fdf")
    files = [text_file, json_file, image_file, video_file, document_file]

    async with uow_cls() as uow:
        await uow.user_files.create(*files)

        response = await uow.user_files.get(*[file.filename for file in files])

        assert response.texts[0].content == text_file
        assert response.jsons[0].content == json_file
        assert response.images[0].content == image_file
        assert response.videos[0].content == video_file
        assert response.documents[0].content == document_file
