from app.application import Application
from app.ui.command import Command


def test_application_registers_default_commands_on_create():
    app = Application.create()

    command = app.services.command_registry.get("hello")

    assert isinstance(command, Command)
    assert command.execute() == "hello"