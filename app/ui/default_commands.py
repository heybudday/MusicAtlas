from __future__ import annotations

from app.ui.command import Command
from app.ui.command_registry import CommandRegistry


def register_default_commands(registry: CommandRegistry) -> None:
    """
    Register built-in application commands.
    """

    registry.register(
        Command(
            name="hello",
            description="Display a greeting.",
            execute=lambda: "hello",
        )
    )

    registry.register(
        Command(
            name="help",
            description="List available commands.",
            execute=lambda: "\n".join(
                command.name
                for command in registry.commands
            ),
        )
    )