from fennflow.repositories import (
    CreateRepository,
    DeletePrefixRepository,
    GeneratePresignedUrlRepository,
    GetRepository,
    PutRepository,
)


class UserFiles(
    PutRepository,
    CreateRepository,
    DeletePrefixRepository,
    GetRepository,
    GeneratePresignedUrlRepository,
):
    pass
