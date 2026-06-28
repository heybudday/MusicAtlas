from app.ui.command import Command
from app.ui.command_registry import CommandRegistry


class HelloCommand(Command):
    def execute(self):
        return "hello"


def test_registry_registers_command():
    registry = CommandRegistry()

    registry.register("hello", HelloCommand())

    assert registry.get("hello").execute() == "hello"


def test_registry_returns_none_for_unknown():
    registry = CommandRegistry()

    assert registry.get("missing") is None