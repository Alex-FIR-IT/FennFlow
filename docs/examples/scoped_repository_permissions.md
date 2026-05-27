# Scoped Repository Permissions

FennFlow's mixin architecture lets each repository expose only the operations it should allow.
Instead of a single god-repository with full access everywhere, you compose exactly the capabilities
each part of your system needs — nothing more.

## Example: Main storage with full access, backup storage with safe write-only access

```python file="examples/scoped_repository_permissions.py"
```

`SafeWriteReadRepository` has no `put` and no `delete` — not restricted at runtime, just never composed in.
Misuse is a `AttributeError` at development time, not a bug in production.