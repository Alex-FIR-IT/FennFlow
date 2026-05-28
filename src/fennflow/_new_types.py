from typing import Any
from uuid import UUID

from typing_extensions import TypeAliasType

from fennflow._sentinel import Omittable

UowQualName = TypeAliasType("UowQualName", str)
StoragePath = TypeAliasType("StoragePath", str)
Namespace = TypeAliasType("Namespace", str)
BackendScope = TypeAliasType("BackendScope", str)
BucketName = Namespace
SessionId = TypeAliasType("SessionId", UUID)

# Connector
ConnectorExtra = Omittable[dict[str, Any]]
