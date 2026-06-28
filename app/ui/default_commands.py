from __future__ import annotations

from app.ui.command import Command
from app.ui.command_registry import CommandRegistry


class HelloCommand(Command):
    """
    Simple built-in UI command used to establish the default command
    registration pattern.
    """

    def __init__(self):
        super().__init__(
            name="hello",
            description="Display a greeting",
            execute=self._execute,
        )

    def _execute(self):
        return "hello"


def register_default_commands(registry: CommandRegistry) -> None:
    """
    Register built-in UI commands with the provided command registry.
    """

    registry.register("hello", HelloCommand())