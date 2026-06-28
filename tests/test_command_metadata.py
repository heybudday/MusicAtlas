from app.ui.command import Command


def test_command_has_metadata():
    command = Command(
        name="hello",
        description="Display a greeting",
        execute=lambda: "hello",
        shortcut="Ctrl+H",
    )

    assert command.name == "hello"
    assert command.description == "Display a greeting"
    assert command.shortcut == "Ctrl+H"
    assert command.execute() == "hello"