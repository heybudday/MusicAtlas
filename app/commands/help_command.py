from __future__ import annotations

from app.ui.command import Command


class HelpCommand(Command):
    def __init__(self, registry):
        super().__init__(
            name="help",
            description="Show available commands",
            usage="help",
            category="General",
        )
        self.registry = registry

    def execute(self, *args):
        requested_category = args[0].strip().lower() if args else None

        commands = self.registry.commands

        if requested_category:
            commands = [
                command
                for command in commands
                if command.category.lower() == requested_category
            ]

            if not commands:
                return f"No commands found in category '{requested_category}'."

        categories = {}

        for command in commands:
            categories.setdefault(command.category, []).append(command)

        output = []

        for category in sorted(categories):
            output.append(category)
            output.append("-" * len(category))

            for command in sorted(categories[category], key=lambda item: item.name):
                output.append(f"{command.name} - {command.description}")
                output.append(f"Usage: {command.usage}")

            output.append("")

        return "\n".join(output).rstrip()