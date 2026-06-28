from __future__ import annotations

from typing import Any, Callable


class Command:
    """
    Represents a user-facing command.

    Commands include both executable behavior and metadata that can be
    used by menus, command palettes, shortcuts, toolbars, and help screens.
    """

    def __init__(
        self,
        *,
        name: str,
        description: str,
        execute: Callable[..., Any],
        shortcut: str | None = None,
    ):
        self.name = name
        self.description = description
        self._execute = execute
        self.shortcut = shortcut

    def execute(self, *args, **kwargs) -> Any:
        return self._execute(*args, **kwargs)