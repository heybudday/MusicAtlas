from app.ui.command import Command
from app.ui.command_registry import CommandRegistry


def test_registry_normalizes_command_names_on_lookup():
    registry = CommandRegistry()

    registry.register(
        Command(
            name="help",
            execute=lambda: "help",
        )
    )

    assert registry.get("HELP").execute() == "help"
    assert registry.get(" Help ").execute() == "help"
    assert registry.get("help ").execute() == "help"