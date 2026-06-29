from __future__ import annotations

from typing import Any

from app.ui.command import Command


class OpenCommand(Command):
    """
    Opens a file via the provided service and returns a formatted string.
    """

    def __init__(self, service: Any):
        self.service = service

        super().__init__(
            name="open",
            description="Opens a file",
            execute=self.execute,
            category="File",
        )

    def execute(self, filename: str) -> str:
        self.service.open(filename)

        return f"opened:{filename}"