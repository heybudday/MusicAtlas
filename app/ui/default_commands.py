from __future__ import annotations

from app.ui.command import Command
from app.ui.command_registry import CommandRegistry
from app.ui.exit_command import ExitCommand


def register_default_commands(registry: CommandRegistry) -> None:
    registry.register(
        Command(
            name="hello",
            execute=lambda: "hello",
            description="Prints a greeting",
        )
    )

    registry.register(
        Command(
            name="help",
            execute=lambda: "\n".join(
                f"{command.name} - {command.description}"
                for command in registry.commands
            ),
            description="Lists available commands",
        )
    )

    registry.register(ExitCommand())