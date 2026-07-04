"""Pure domain logic: composing greetings."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Greeter:
    """Builds greetings for a named audience.

    Immutable; configure the salutation at construction time.
    """

    salutation: str = "Hello"

    def greet(self, name: str) -> str:
        """Return the greeting for ``name``, with surrounding whitespace stripped.

        Raises:
            ValueError: if ``name`` is blank.
        """
        cleaned = name.strip()
        if not cleaned:
            raise ValueError("name must not be blank")
        return f"{self.salutation}, {cleaned}!"
