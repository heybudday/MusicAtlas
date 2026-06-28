from __future__ import annotations

from typing import Any

from app.ui.command_registry import CommandRegistry


class CommandDispatcher:
    """
    Routes command names to registered Command objects.
    """

    def __init__(self, registry: CommandRegistry):
        self._registry = registry

    def dispatch(self, command_name: str, *args, **kwargs) -> Any:
        command = self._registry.get(command_name)
        return command.execute(*args, **kwargs)

    def has_command(self, command_name: str) -> bool:
        return self._registry.has(command_name)