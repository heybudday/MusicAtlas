from __future__ import annotations


class CommandError(Exception):
    pass


class ValidationError(CommandError):
    pass


class CommandExecutionError(CommandError):
    pass