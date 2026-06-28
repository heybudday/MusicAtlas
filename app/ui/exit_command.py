from __future__ import annotations

from app.ui.command import Command


class ExitCommand(Command):
    def __init__(self):
        super().__init__(
            name="exit",
            description="Exits the application",
            execute=self._execute,
        )

    def _execute(self):
        return False