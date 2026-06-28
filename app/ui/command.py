from __future__ import annotations

from typing import Any, Callable


class Command:
    """
    Represents a user-facing command.
    """

    def __init__(
        self,
        name: str,
        execute: Callable[..., Any],
        description: str = "",
        shortcut: str | None = None,
        aliases: list[str] | None = None,
    ):
        self.name = name
        self._execute = execute
        self.description = description
        self.shortcut = shortcut
        self.aliases = aliases or []

    def execute(self, *args, **kwargs) -> Any:
        return self._execute(*args, **kwargs)