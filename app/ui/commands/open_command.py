from __future__ import annotations

from app.ui.command import Command


class OpenCommand(Command):
    """
    Opens a report or file through the archive service.
    """

    name = "open"
    description = "Open a report."

    def __init__(self, archive_service):
        self.archive_service = archive_service

    def execute(self, name: str):
        return self.archive_service.open(name)