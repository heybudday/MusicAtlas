from __future__ import annotations

from app.ui.command import Command
from app.ui.command_dispatcher import CommandDispatcher
from app.ui.command_registry import CommandRegistry
from app.ui.errors import CommandExecutionError, ValidationError


def test_dispatcher_returns_validation_error_message():
    registry = CommandRegistry()

    def execute(*args):
        raise ValidationError("Missing required argument: report_id")

    registry.register(Command(name="open", execute=execute))

    dispatcher = CommandDispatcher(registry)

    assert dispatcher.dispatch("open") == "Missing required argument: report_id"


def test_dispatcher_returns_execution_error_message():
    registry = CommandRegistry()

    def execute(*args):
        raise CommandExecutionError("Could not open report")

    registry.register(Command(name="open", execute=execute))

    dispatcher = CommandDispatcher(registry)

    assert dispatcher.dispatch("open report_123") == "Could not open report"


def test_dispatcher_hides_unexpected_exceptions():
    registry = CommandRegistry()

    def execute(*args):
        raise RuntimeError("database exploded")

    registry.register(Command(name="open", execute=execute))

    dispatcher = CommandDispatcher(registry)

    assert dispatcher.dispatch("open report_123") == "An unexpected error occurred."