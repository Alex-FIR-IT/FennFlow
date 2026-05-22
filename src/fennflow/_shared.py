from fennflow._operations.enums import OperationTypeEnum

inserting_types = {
    OperationTypeEnum.CREATE,
    OperationTypeEnum.PUT,
}
unique_constraint = ("scope", "namespace", "storage_path")
