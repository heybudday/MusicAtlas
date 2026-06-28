from app.services.service_registry import ServiceRegistry
from app.ui.command_registry import CommandRegistry
from app.ui.default_commands import register_default_commands
from app.ui.command_dispatcher import CommandDispatcher
from app.desktop.desktop_shell import DesktopShell


class OpenFileService:
    def open(self, filename: str) -> None:
        return None


class Application:
    def __init__(self):
        self.services = ServiceRegistry()

        self.services.command_registry = CommandRegistry()
        self.services.open_file_service = OpenFileService()

        register_default_commands(
            self.services.command_registry,
            self.services.open_file_service,
        )

        self.dispatcher = CommandDispatcher(self.services.command_registry)

        self.shell = DesktopShell(self)

    @classmethod
    def create(cls):
        return cls()