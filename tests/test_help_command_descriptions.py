from app.ui.command_registry import CommandRegistry
from app.ui.default_commands import register_default_commands


def test_help_command_shows_descriptions():
    registry = CommandRegistry()

    register_default_commands(registry)

    help_command = registry.get("help")

    assert help_command.execute() == (
        "hello - Prints a greeting\n"
        "help - Lists available commands\n"
        "exit - Exits the application"
    )