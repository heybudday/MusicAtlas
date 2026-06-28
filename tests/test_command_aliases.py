from app.ui.command import Command
from app.ui.command_registry import CommandRegistry


def test_registry_resolves_command_aliases():
    registry = CommandRegistry()

    registry.register(
        Command(
            name="help",
            execute=lambda: "help",
            aliases=["h", "?"],
        )
    )

    assert registry.get("help").execute() == "help"
    assert registry.get("h").execute() == "help"
    assert registry.get("?").execute() == "help"