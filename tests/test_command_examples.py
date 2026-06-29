from app.ui.command import Command


def test_command_examples_defaults_to_empty_list():
    command = Command("hello", lambda: None)

    assert command.examples == []