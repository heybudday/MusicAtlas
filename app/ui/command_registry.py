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

        self._commands[name] = command

        for alias in getattr(command, "aliases", []):
            self._aliases[alias] = name

    def get(self, command_name: str) -> Command | None:
        resolved_name = self._aliases.get(command_name, command_name)

        return self._commands.get(resolved_name)

    @property
    def commands(self) -> list[Command]:
        return list(self._commands.values())

    def list_commands(self) -> list[Command]:
        return self.commands