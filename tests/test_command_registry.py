from app.ui.command import Command
from app.ui.command_registry import CommandRegistry


class HelloCommand(Command):
    def __init__(self):
        super().__init__(
            name="hello",
            description="Display a greeting",
            execute=self._execute,
        )

    def _execute(self):
        return "hello"


def test_registry_registers_command():
    registry = CommandRegistry()

    registry.register("hello", HelloCommand())

    assert registry.get("hello").execute() == "hello"


def test_registry_returns_none_for_missing_command():
    registry = CommandRegistry()

    assert registry.get("missing") is None