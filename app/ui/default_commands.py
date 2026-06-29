from __future__ import annotations

from app.ui.command import Command
from app.ui.commands.open_command import OpenCommand


def hello(*args):
    return "hello"


def exit_command(*args):
    return False


class HelpCommand(Command):
    def __init__(self, registry):
        super().__init__(
            name="help",
            execute=self.execute_help,
            description="Show available commands",
            category="General",
            usage="help",
        )
        self.registry = registry

    def execute_help(self, *args):
        requested_category = args[0].strip().lower() if args else None

        commands = self.registry.commands

        if requested_category:
            commands = [
                command
                for command in commands
                if (command.category or "General").lower() == requested_category
            ]

            if not commands:
                return f"No commands found in category '{requested_category}'."

        sections = {}

        for command in commands:
            category = command.category or "General"
            sections.setdefault(category, []).append(command)

        lines = []

        for category in sorted(sections):
            lines.append(category)
            lines.append("-" * len(category))

            for command in sorted(sections[category], key=lambda item: item.name):
                description = command.description or ""
                usage = command.usage or command.name

                if description:
                    lines.append(f"{command.name} - {description}")
                else:
                    lines.append(command.name)

                lines.append(f"Usage: {usage}")

            lines.append("")

        return "\n".join(lines).strip()


def register_default_commands(registry, open_file_service):
    registry.register(
        Command(
            name="hello",
            execute=hello,
            description="Say hello",
            category="General",
            usage="hello",
        )
    )
    registry.register(HelpCommand(registry))
    registry.register(OpenCommand(open_file_service))
    registry.register(
        Command(
            name="exit",
            execute=exit_command,
            description="Exit the application",
            category="System",
            usage="exit",
        )
    )