from __future__ import annotations

from collections.abc import Callable
from typing import Any


class CommandDispatcher:
    def __init__(self) -> None:
        self._commands: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, handler: Callable[..., Any]) -> None:
        self._commands[name] = handler

    def dispatch(self, name: str, *args: Any, **kwargs: Any) -> Any:
        if name not in self._commands:
            raise KeyError(f"Unknown command: {name}")

        return self._commands[name](*args, **kwargs)