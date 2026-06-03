from fennflow.repositories import (
    CreateRepository,
    DeletePrefixRepository,
    DeleteRepository,
    GeneratePresignedUrlPrefixRepository,
    GeneratePresignedUrlRepository,
    GetPrefixRepository,
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
    GetPrefixRepository,
    GeneratePresignedUrlRepository,
    GeneratePresignedUrlPrefixRepository,
):
    pass
