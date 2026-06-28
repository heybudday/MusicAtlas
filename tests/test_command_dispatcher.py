import pytest

from app.command_dispatcher import CommandDispatcher


def test_can_register_command():
    dispatcher = CommandDispatcher()

    dispatcher.register("test", lambda: "ok")

    assert "test" in dispatcher._commands


def test_dispatch_calls_handler():
    dispatcher = CommandDispatcher()

    called = {"value": False}

    def handler():
        called["value"] = True

    dispatcher.register("test", handler)

    dispatcher.dispatch("test")

    assert called["value"] is True


def test_dispatch_returns_handler_result():
    dispatcher = CommandDispatcher()

    dispatcher.register("answer", lambda: 42)

    assert dispatcher.dispatch("answer") == 42


def test_unknown_command_raises_key_error():
    dispatcher = CommandDispatcher()

    with pytest.raises(KeyError):
        dispatcher.dispatch("missing")