from __future__ import annotations

import shlex


class CommandDispatcher:
    def __init__(self, registry):
        self.registry = registry

    def dispatch(self, command_line: str):
        parts = shlex.split(command_line)

        if not parts:
            return None

        command_name = parts[0]
        args = parts[1:]

        command = self.registry.get(command_name)

        if command is None:
            return f"Unknown command: {command_name}"

        if command.validator:
            result = command.validator.validate(args)

            if not result.valid:
                return result.message

        return command(*args)