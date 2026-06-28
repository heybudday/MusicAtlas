from __future__ import annotations

from app.ui.command import Command


class ExitCommand(Command):
    """
    Terminates the application.
    """

    def __init__(self):
        super().__init__(
            name="exit",
            execute=self.execute,
            description="Exits the application",
        )

    def execute(self) -> bool:
        return False