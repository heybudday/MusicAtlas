from __future__ import annotations

from app.ui.command import Command


class HistoryCommand(Command):
    def __init__(self, history):
        super().__init__(
            name="history",
            execute=self.execute_history,
            description="Show command history",
            usage="history",
        )

        self.history = history

    def execute_history(self, *args):
        lines = []

        for index, command in enumerate(self.history.commands, start=1):
            lines.append(f"{index}  {command}")

        return "\n".join(lines)