from app.ui.command import Command


def test_command_has_usage():
    command = Command(
        name="open",
        execute=lambda: None,
        usage="open <filename>",
    )

    assert command.usage == "open <filename>"