from app.ui.command import Command
from app.ui.command_registry import CommandRegistry


class TestCommand(Command):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def execute(self):
        return self._name


def test_registry_lists_registered_commands():
    registry = CommandRegistry()

    hello = TestCommand("hello")
    open_command = TestCommand("open")
    exit_command = TestCommand("exit")

    registry.register(hello)
    registry.register(open_command)
    registry.register(exit_command)

    assert registry.list_commands() == [
        hello,
        open_command,
        exit_command,
    ]


def test_registry_exposes_commands_property():
    registry = CommandRegistry()

    hello = TestCommand("hello")

    registry.register(hello)

    assert registry.commands == [hello]