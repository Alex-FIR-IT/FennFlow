# Saga Compensation in Action

FennFlow's Unit of Work automatically rolls back all pending operations if something goes wrong.
Combined with `auto_commit=False`, you get full control over when a transaction is committed —
making it trivial to tie file storage to the result of an external service call.

## Example: Upload avatar and verify with external face verification API

```python file="examples/saga_compensation.py"
```

No manual cleanup code. No try/finally. If the verification API rejects the image or raises an exception,
the UoW exits without a commit and the uploaded avatar is automatically compensated out of S3.
You can use auto_commit=True and call uow.rollback on failure as well.