from app.application import Application
from app.ui.command_completion import CommandCompletion


def test_completion_returns_matching_commands():
    app = Application.create()

    completion = CommandCompletion(app.services.command_registry)

    assert completion.complete("") == [
        "exit",
        "hello",
        "help",
    ]

    assert completion.complete("h") == [
        "hello",
        "help",
    ]

    assert completion.complete("hel") == [
        "hello",
        "help",
    ]

    assert completion.complete("helt") == []

    assert completion.complete("xyz") == []