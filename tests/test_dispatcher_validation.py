from app.ui.command import Command
from app.ui.command_dispatcher import CommandDispatcher
from app.ui.command_registry import CommandRegistry
from app.ui.validation import RequiredArgumentsValidator


def test_dispatcher_does_not_execute_when_validation_fails():
    executed = False

    def execute(*args):
        nonlocal executed
        executed = True
        return "executed"

    registry = CommandRegistry()
    registry.register(
        Command(
            name="open",
            execute=execute,
            validator=RequiredArgumentsValidator(1),
        )
    )

    dispatcher = CommandDispatcher(registry)

    result = dispatcher.dispatch("open")

    assert result == "Expected at least 1 argument(s)."
    assert executed is False


def test_dispatcher_executes_when_validation_passes():
    executed = False

    def execute(*args):
        nonlocal executed
        executed = True
        return "success"

    registry = CommandRegistry()
    registry.register(
        Command(
            name="open",
            execute=execute,
            validator=RequiredArgumentsValidator(1),
        )
    )

    dispatcher = CommandDispatcher(registry)

    result = dispatcher.dispatch("open file.txt")

    assert result == "success"
    assert executed is True