from __future__ import annotations

from app.ui.command import Command


class CommandRegistry:
    """
    Stores and resolves user-facing commands.
    """

    def __init__(self):
        self._commands: dict[str, Command] = {}
        self._aliases: dict[str, str] = {}

    def register(self, *args) -> None:
        if len(args) == 1:
            command = args[0]
            name = command.name
        elif len(args) == 2:
            name, command = args
        else:
            raise TypeError("register() expects (command) or (name, command)")

        normalized_name = self._normalize(name)
        self._commands[normalized_name] = command

        for alias in getattr(command, "aliases", []):
            self._aliases[self._normalize(alias)] = normalized_name

    def get(self, command_name: str) -> Command | None:
        normalized_name = self._normalize(command_name)
        resolved_name = self._aliases.get(normalized_name, normalized_name)

        return self._commands.get(resolved_name)

    @property
    def commands(self) -> list[Command]:
        return list(self._commands.values())

    def list_commands(self) -> list[Command]:
        return self.commands

    def _normalize(self, command_name: str) -> str:
        return command_name.strip().lower()