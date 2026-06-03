from fennflow.repositories import (
    CreateRepository,
    DeletePrefixRepository,
    DeleteRepository,
    GeneratePresignedUrlRepository,
    GetRepository,
    ListRepository,
    PutRepository,
)


class UserFiles(
    ListRepository,
    PutRepository,
    CreateRepository,
    DeleteRepository,
    DeletePrefixRepository,
    GetRepository,
    GeneratePresignedUrlRepository,
):
    pass
