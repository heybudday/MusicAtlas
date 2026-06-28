from __future__ import annotations

from app.command_dispatcher import CommandDispatcher
from app.services.service_registry import ServiceRegistry


class Application:
    """
    Application bootstrap.

    Responsible for constructing and exposing shared services through
    a single ServiceRegistry instance and routing named commands through
    a CommandDispatcher.

    Future desktop, mobile, API, and CLI entry points should construct
    one Application and obtain services or dispatch commands from it.
    """

    def __init__(self):
        self._registry = ServiceRegistry()
        self._dispatcher = CommandDispatcher()

    @property
    def services(self) -> ServiceRegistry:
        return self._registry

    @property
    def dispatcher(self) -> CommandDispatcher:
        return self._dispatcher

    def dispatch(self, command_name: str, *args, **kwargs):
        return self._dispatcher.dispatch(command_name, *args, **kwargs)

    @classmethod
    def create(cls) -> "Application":
        """
        Factory method used by application entry points.
        """
        return cls()