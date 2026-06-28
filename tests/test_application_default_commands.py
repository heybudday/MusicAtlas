from app.application import Application


def test_application_registers_default_commands():
    app = Application.create()

    commands = app.services.command_registry.commands

    assert [command.name for command in commands] == ["hello", "help"]