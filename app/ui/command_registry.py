from __future__ import annotations

from app.ui.command import Command


class CommandRegistry:
    """
    Registry for UI commands.
    """

    def __init__(self):
        self._commands: dict[str, Command] = {}

    def register(self, *args) -> None:
        if len(args) == 1:
            command = args[0]
            self._commands[command.name] = command
            return

        if len(args) == 2:
            command_name, command = args
            self._commands[command_name] = command
            return

        raise TypeError("register() expects a Command or (name, Command)")

    def get(self, command_name: str) -> Command | None:
        return self._commands.get(command_name)

    def has_command(self, command_name: str) -> bool:
        return command_name in self._commands

    def list_commands(self) -> list[Command]:
        return list(self._commands.values())

    @property
    def commands(self) -> list[Command]:
        return self.list_commands()