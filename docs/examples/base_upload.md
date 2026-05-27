# Working with File Content

FennFlow wraps raw bytes in typed content models. Instead of juggling `bytes` and `dict`,
you work with `TextContent`, `JsonContent`, `BinaryContent` and others — each with typed accessors
for their data.

## Example: Creating, uploading and retrieving typed files

```python file="examples/base_upload.py"
```

`TextContent.content` returns a `str`, `JsonContent.content` returns the parsed Python object —
no manual `decode()` or `json.loads()` needed.

MediaResponse uses `ContentFactory` to resolve the correct class on retrieval
automatically based on the stored MIME type, so `.texts`, `.filter()`, `.filter_by_media_type()` and other
typed accessors on `MediaResponse` always return the right types.
