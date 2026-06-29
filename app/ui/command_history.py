from __future__ import annotations


class CommandHistory:
    def __init__(self):
        self._commands = []

    def add(self, command_line: str):
        self._commands.append(command_line)

    @property
    def commands(self):
        return list(self._commands)