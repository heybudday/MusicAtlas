from app.ui.command import Command


def test_command_has_description():
    command = Command(
        name="hello",
        execute=lambda: "hello",
        description="Prints a greeting",
    )

    assert command.description == "Prints a greeting"