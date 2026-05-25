# Backends

A backend stores **operation metadata** — which files exist, their current status, and which session owns a pending
operation. It is the source of truth for FennFlow: if a file is not in the backend, it is invisible to the UoW
regardless of what the file storage contains.

Backends do not store file data. That is the connector's responsibility.

## Why a separate backend?

Raw file storage (S3, etc.) has no concept of pending operations, sessions, or compensation. The backend gives FennFlow
a consistent view of state that it can query and update independently of the storage. This is what makes the Saga
flow possible: the backend is always consulted before any storage operation, and its state is what commit and rollback
act on.

## SQLAlchemyBackend

The default backend. Stores metadata in a database via SQLAlchemy. Defaults to a local SQLite file
(`fennflow.db`) with no external infrastructure required.

```python
from fennflow.backends import SqlalchemyBackendConfig


class UOW(UnitOfWork):
    config = ConfigDict(
        backend=SqlalchemyBackendConfig(),
        )
```

`SqlalchemyBackendConfig` accepts the following fields:

- `database_url` — any SQLAlchemy-compatible async URL. Defaults to `sqlite+aiosqlite:///fennflow.db`.
  Requires `aiosqlite` to be installed. Pass an explicit URL to use a different database.
- `db_schema` — schema name for FennFlow's tables. Defaults to `"fennflow"`.
- `table_name` — table name for metadata records. Defaults to `"metadata"`.
- `scope` — label to isolate backend state. Defaults to `"default"`. Use different scopes when
  running multiple UoW classes in the same process that point to different storage instances, to prevent
  their metadata from merging.

```python
from fennflow.backends import SqlalchemyBackendConfig


class AWSUOW(UnitOfWork):
    config = ConfigDict(
        backend=SqlalchemyBackendConfig(scope="aws"),
        )


class MinIOUOW(UnitOfWork):
    config = ConfigDict(
        backend=SqlalchemyBackendConfig(scope="minio"),
        )
```

For testing, point the backend at an in-memory SQLite database — no files created, no cleanup needed:

```python
from fennflow.backends import SqlalchemyBackendConfig


class TestUOW(AppUOW):
    config = ConfigDict(
        backend=SqlalchemyBackendConfig(database_url="sqlite+aiosqlite:///:memory:"),
        )
```

## Implementing a custom backend

Subclass `AbstractBackend`, create a factory and register it in `backend_registry`.

For available and planned backends, see the [roadmap](https://github.com/users/Alex-FIR-IT/projects/2/views/2).

If you need a backend that isn't there, [open an issue](https://github.com/Alex-FIR-IT/FennFlow/issues).