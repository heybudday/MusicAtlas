from __future__ import annotations

from app.ui.command import Command


class CommandRegistry:
    """
    Registry for named UI commands.
    """

    def __init__(self):
        self._commands: dict[str, Command] = {}

    def register(self, name: str, command: Command) -> None:
        self._commands[name] = command

    def get(self, name: str) -> Command | None:
        return self._commands.get(name)