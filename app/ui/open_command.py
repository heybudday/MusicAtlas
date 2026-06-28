from app.ui.command import Command


class OpenCommand(Command):
    def __init__(self):
        super().__init__(
            name="open",
            execute=self._execute,
            description="Opens a report file"
        )

    def _execute(self, filename: str):
        return f"opened {filename}"