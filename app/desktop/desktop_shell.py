from __future__ import annotations

from app.application import Application
from app.services.service_registry import ServiceRegistry


class DesktopShell:
    """
    Initial desktop shell abstraction.

    This gives future desktop UI code a stable place to access the
    application, services, and command dispatcher.
    """

    def __init__(self, application: Application):
        self.application = application
        self.services = application.services
        self.dispatcher = application.dispatcher

    def run(self) -> bool:
        return True

    def run_command(self, command_name: str, *args, **kwargs):
        return self.dispatcher.dispatch(command_name, *args, **kwargs)