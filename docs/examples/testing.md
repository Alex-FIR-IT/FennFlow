# Testing with FennFlow

FennFlow is designed to be testable without mocks. Swap `S3ConnectorConfig` for
`InMemoryConnectorConfig` and point the backend at an in-memory SQLite database —
your tests run with zero infrastructure and zero mocks.

## Example: Testing user registration with avatar upload

```python file="examples/testing.py"
```

`TestUOW` inherits everything from `AppUOW` and overrides only the config — same repositories,
same business logic, different infrastructure. No mocks, no patching, no Docker.