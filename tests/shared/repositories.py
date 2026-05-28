from fennflow.repositories import (
    CreateRepository,
    DeleteRepository,
    GeneratePresignedUrlRepository,
    GetRepository,
    ListRepository,
    PutRepository,
)


class UserFiles(
    PutRepository,
    CreateRepository,
    DeleteRepository,
    GetRepository,
    ListRepository,
    GeneratePresignedUrlRepository,
):
    pass
