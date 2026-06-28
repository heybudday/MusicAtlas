from __future__ import annotations

from collections.abc import Callable
from typing import Any

from app.application import Application
from app.services.service_registry import ServiceRegistry
from app.ui.command_dispatcher import CommandDispatcher


class DesktopShell:
    """
    Desktop application shell.

    Owns desktop-facing behavior while delegating shared application
    services to the Application instance.
    """

    def __init__(self, application: Application):
        self.application = application
        self.services: ServiceRegistry = application.services
        self.dispatcher: CommandDispatcher = application.dispatcher

    def run(
        self,
        input_func: Callable[[str], str] | None = None,
        output_func: Callable[[Any], None] = print,
    ) -> bool:
        if input_func is None:
            return True

        while True:
            result = self.process_input(input_func("> "))

            if result is False:
                return True

            if result is not None:
                output_func(result)

    def execute_command(self, command_name: str):
        command = self.services.command_registry.get(command_name)

        if command is None:
            return None

        return command.execute()

    def process_input(self, user_input: str):
        result = self.execute_command(user_input.strip().lower())

        if result is None:
            return f"Unknown command: {user_input}"

        return result