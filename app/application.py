from __future__ import annotations

from app.services.service_registry import ServiceRegistry
from app.ui.command_dispatcher import CommandDispatcher
from app.ui.default_commands import register_default_commands


class Application:
    """
    Application bootstrap.

    Responsible for constructing and exposing shared services through
    a single ServiceRegistry instance.

    Future desktop, mobile, API, and CLI entry points should construct
    one Application and obtain services from it.
    """

    def __init__(self):
        self._registry = ServiceRegistry()
        register_default_commands(self._registry.command_registry)
        self.dispatcher = CommandDispatcher(self._registry.command_registry)

    @property
    def services(self) -> ServiceRegistry:
        return self._registry

    @classmethod
    def create(cls) -> "Application":
        """
        Factory method used by application entry points.
        """
        return cls()