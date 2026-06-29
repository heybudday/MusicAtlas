from __future__ import annotations

from app.ui.errors import CommandError


class CommandDispatcher:
    def __init__(self, registry):
        self.registry = registry

    def dispatch(self, command_line: str):
        parts = command_line.strip().split()

        if not parts:
            return None

        command_name = parts[0]
        args = parts[1:]

        command = self.registry.get(command_name)

        if command is None:
            return f"Unknown command: {command_name}"

        try:
            validation_result = command.validate(*args)

            if not validation_result.valid:
                return validation_result.message

            return command.execute(*args)

        except CommandError as ex:
            return str(ex)

        except Exception:
            return "An unexpected error occurred."