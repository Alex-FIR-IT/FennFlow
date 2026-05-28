from typing import Protocol, runtime_checkable


@runtime_checkable
class PathTemplate(Protocol):
    """Protocol for typed path templates used with ``AtRepository.at()``.

    Implement this protocol to define reusable, parameterized storage paths.
    Any class with a ``render() -> str`` method satisfies this protocol — no
    inheritance or registration required.

    Example::

        from dataclasses import dataclass


        @dataclass
        class PassportPath:
            user_id: int

            def render(self) -> str:
                return f"credentials/user_{self.user_id}/passport"


        async with AppUOW() as uow:
            await uow.credentials.at(PassportPath(user_id=42)).put(passport)
    """

    def render(self) -> str:
        """Return the resolved path string for this template.

        Returns:
            A non-empty string representing the storage path segment.
            Trailing slashes are normalized by ``at()`` and may be omitted.
        """
        ...
