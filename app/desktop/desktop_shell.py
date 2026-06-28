from __future__ import annotations

from app.application import Application
from app.command_dispatcher import CommandDispatcher
from app.services.service_registry import ServiceRegistry


class DesktopShell:
    """
    Minimal desktop application shell.

    This class is the first desktop-facing entry point for Music Atlas.
    It wraps the shared Application core and exposes the shared services
    and command dispatcher needed by future desktop UI implementations.
    """

    def __init__(self, application: Application):
        self._application = application
        self._dispatcher = application.dispatcher

    @property
    def application(self) -> Application:
        return self._application

    @property
    def services(self) -> ServiceRegistry:
        return self._application.services

    @property
    def dispatcher(self) -> CommandDispatcher:
        return self._dispatcher

    def run(self) -> bool:
        """
        Start the desktop shell.

        For MA-075 this is intentionally minimal. A future ticket can
        replace this stub with a real GUI event loop.
        """
        return True