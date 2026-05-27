# Using Multiple Connectors

FennFlow makes it trivial to work with multiple object storages simultaneously. Each `UnitOfWork` owns
its own connector and backend scope, so you can compose them freely in the same coroutine.

## Example: Migrating files from AWS S3 to MinIO

```python file="examples/multiple_connectors.py"
```

The two UoWs are fully independent — different credentials, different endpoints, different backend scopes.
If anything fails mid-transfer, each UoW rolls back its own pending operations independently.