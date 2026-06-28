from app.ui.command import Command
from app.ui.exit_command import ExitCommand
from app.ui.open_command import OpenCommand


def register_default_commands(registry):
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

    # FIX: ensure OpenCommand exists
    registry.register(OpenCommand())

    registry.register(ExitCommand())