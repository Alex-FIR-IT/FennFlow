# Path Templates

Raw S3 paths scattered across a codebase are a maintenance problem. A path like
`credentials/user_id_123/passport` written inline in five different places is five
places to update when the layout changes, and five places to introduce a typo.

Path templates solve this by centralizing path construction logic in a single,
typed, testable place — without adding any fancy magic concepts.

## The Problem

`.at()` accepts a plain string, which means path construction is entirely the
caller's responsibility:

```python
async with AppUOW() as uow:
    await uow.credentials.at(f"credentials/user_id_{user_id}/passport").put(passport)
```

This works, but it pushes path knowledge into call sites. Any refactor of your
storage layout requires hunting down every string.

## PathTemplate Protocol

FennFlow provides a minimal protocol for path templates:

```python
from fennflow.path_template import PathTemplate
```

```python
class PathTemplate(Protocol):
    def render(
            self
            ) -> str: ...
```

`.at()` accepts either a `str` or any object that satisfies `PathTemplate` — i.e.
any object with a `render() -> str` method. No base class to inherit, no
registration required.

## Defining Templates

Define your templates as plain dataclasses in your application code and then use them directly with .at():

```python file="examples/path_templates.py"
```

The IDE resolves `AvatarPath(user_id=user_id)` as a typed constructor. Mypy checks
the field types. Autocomplete works on all template fields. If `user_id` changes
type or a new required field is added, the type checker catches every broken call
site immediately.

## Multi-Parameter Templates

Templates are dataclasses — they can hold as many fields as needed:

```python
@dataclass(slots=True)
class ReportPath:
    org_id: int
    year: int
    month: int

    def render(
            self
            ) -> str:
        return f"reports/org_{self.org_id}/{self.year}/{self.month:02d}"
```

```python
await uow.reports.at(ReportPath(org_id=1, year=2025, month=6)).put(report)
```

## Chaining Templates

Since `.at()` is chainable and templates are just another form of path segment,
templates and plain strings can be mixed and chained freely:

```python
@dataclass(slots=True)
class UserPrefix:
    user_id: int

    def render(
            self
            ) -> str:
        return f"users/user_{self.user_id}"


@dataclass(slots=True)
class YearMonth:
    year: int
    month: int

    def render(
            self
            ) -> str:
        return f"{self.year}/{self.month:02d}"
```

```python
async with AppUOW() as uow:
    # two templates chained
    await uow.files.at(UserPrefix(user_id=1)).at(YearMonth(year=2025, month=6)).put(report)

    # template chained with a plain string
    await uow.files.at(UserPrefix(user_id=1)).at("archive").put(backup)
```
