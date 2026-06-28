from app.ui.command import Command


class HelloCommand(Command):
    def __init__(self):
        super().__init__(
            name="hello",
            description="Display a greeting",
            execute=self._execute,
        )

    def _execute(self):
        return "hello"


def test_command_execute():
    command = HelloCommand()

    assert command.execute() == "hello"