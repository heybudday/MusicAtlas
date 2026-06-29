from __future__ import annotations

from typing import Any

from app.ui.command import Command
from app.ui.commands.history_command import HistoryCommand
from app.ui.commands.open_command import OpenCommand
from app.ui.exit_command import ExitCommand


def register_default_commands(
    registry,
    open_file_service: Any | None = None,
    command_history=None,
):
    registry.register(
        Command(
            name="hello",
            description="Prints a greeting",
            execute=lambda: "hello",
        )
    )

    registry.register(
        Command(
            name="help",
            description="Lists available commands",
            execute=lambda: "\n".join(
                f"{c.name} - {c.description}"
                for c in registry.commands
                if c.name in {"hello", "help", "exit", "history"}
            ),
        )
    )

    registry.register(ExitCommand())

    if open_file_service is not None:
        registry.register(OpenCommand(open_file_service))

    if command_history is not None:
        registry.register(HistoryCommand(command_history))