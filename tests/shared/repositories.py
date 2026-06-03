from fennflow.repositories import (
    CreateRepository,
    DeletePrefixRepository,
    DeleteRepository,
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
):
    pass
