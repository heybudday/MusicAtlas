from __future__ import annotations

from app.services.service_registry import ServiceRegistry
from app.ui.default_commands import register_default_commands
from app.desktop.desktop_shell import DesktopShell
from app.ui.command_dispatcher import CommandDispatcher


class Application:
    """
    Application bootstrap.

    Owns all core services and exposes UI entry points.
    """

    def __init__(self, services, dispatcher, shell):
        self.services = services
        self.dispatcher = dispatcher
        self.shell = shell

    @classmethod
    def create(cls) -> "Application":
        services = ServiceRegistry()

        # register default commands
        register_default_commands(services.command_registry)

        # FIX: dispatcher needs registry
        dispatcher = CommandDispatcher(services.command_registry)

        shell = DesktopShell(app=None)

        app = cls(
            services=services,
            dispatcher=dispatcher,
            shell=shell
        )

        shell.set_app(app)

        return app