from __future__ import annotations

from typing import Any, Callable


class CommandDispatcher:
    """
    Routes named commands to registered callables.
    """

    def __init__(self):
        self._commands: dict[str, Callable[..., Any]] = {}

    def register(self, command_name: str, handler: Callable[..., Any]) -> None:
        self._commands[command_name] = handler

    def dispatch(self, command_name: str, *args, **kwargs) -> Any:
        if command_name not in self._commands:
            raise KeyError(f"Unknown command: {command_name}")

        return self._commands[command_name](*args, **kwargs)

    def has_command(self, command_name: str) -> bool:
        return command_name in self._commands