from app.ui.command import Command
from app.ui.command_dispatcher import CommandDispatcher
from app.ui.command_history import CommandHistory
from app.ui.command_registry import CommandRegistry
from app.ui.validation import ValidationResult


class InvalidValidator:
    def validate(self, args):
        return ValidationResult(False, "invalid")


def test_successful_commands_are_recorded():
    history = CommandHistory()
    registry = CommandRegistry()

    registry.register(
        Command(
            name="hello",
            execute=lambda: "hello",
        )
    )

    dispatcher = CommandDispatcher(registry, history)

    dispatcher.dispatch("hello")

    assert history.commands == ["hello"]


def test_validation_failures_are_not_recorded():
    history = CommandHistory()
    registry = CommandRegistry()

    registry.register(
        Command(
            name="hello",
            execute=lambda: "hello",
            validator=InvalidValidator(),
        )
    )

    dispatcher = CommandDispatcher(registry, history)

    dispatcher.dispatch("hello")

    assert history.commands == []


def test_unknown_commands_are_not_recorded():
    history = CommandHistory()
    registry = CommandRegistry()

    dispatcher = CommandDispatcher(registry, history)

    dispatcher.dispatch("unknown")

    assert history.commands == []