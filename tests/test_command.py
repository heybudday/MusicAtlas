from app.ui.command import Command


class HelloCommand(Command):
    def execute(self):
        return "hello"


def test_command_execute():
    command = HelloCommand()

    assert command.execute() == "hello"