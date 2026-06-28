from app.ui.command import Command
from app.ui.command_dispatcher import CommandDispatcher
from app.ui.command_registry import CommandRegistry


class TestCommand(Command):
    def __init__(self):
        super().__init__(
            name="test",
            description="Test command",
            execute=self._execute,
        )

    def _execute(self):
        return "ran"


def test_dispatcher_executes_registered_command_object():
    registry = CommandRegistry()
    registry.register("test", TestCommand())

    dispatcher = CommandDispatcher(registry)

    assert dispatcher.dispatch("test") == "ran"