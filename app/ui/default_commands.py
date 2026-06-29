from __future__ import annotations

from app.ui.command import Command
from app.ui.command_registry import CommandRegistry
from app.ui.exit_command import ExitCommand


def format_help(commands: list[Command]) -> str:
    lines: list[str] = []
    seen_categories: list[str] = []

    for command in commands:
        if command.category not in seen_categories:
            seen_categories.append(command.category)

    for category in seen_categories:
        if lines:
            lines.append("")

        lines.append(category)
        lines.append("-" * len(category))

        for command in commands:
            if command.category == category:
                lines.append(command.name)

    return "\n".join(lines)


def register_default_commands(
    registry: CommandRegistry,
    open_file_service,
) -> None:
    registry.register(
        Command(
            name="hello",
            execute=lambda: "hello",
            description="Prints a greeting",
            category="General",
        )
    )

    registry.register(
        Command(
            name="help",
            execute=lambda: format_help(registry.commands),
            description="Lists available commands",
            category="General",
        )
    )

    registry.register(
        Command(
            name="open",
            execute=lambda filename: _open_file(open_file_service, filename),
            description="Opens a file",
            category="File",
        )
    )

    registry.register(ExitCommand())


def _open_file(open_file_service, filename: str) -> str:
    open_file_service.open(filename)

    return f"opened:{filename}"