from __future__ import annotations


class DesktopShell:
    """
    Desktop shell entry point.
    """

    def __init__(self, app=None):
        self.app = app
        self.dispatcher = app.dispatcher if app else None
        self.services = app.services if app else None

    def set_app(self, app):
        self.app = app
        self.dispatcher = app.dispatcher
        self.services = app.services

    def run_once(self, input_line: str):
        parts = input_line.strip().split()

        if not parts:
            return None

        command_name = parts[0]
        args = parts[1:]

        return self.dispatcher.dispatch(command_name, *args)