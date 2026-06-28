from __future__ import annotations


class ApplicationShell:
    """
    Framework-agnostic application shell.

    Receives high-level commands and delegates execution to the
    application's command registry or dispatcher.
    """

    def __init__(self, registry):
        self._registry = registry

    def dispatch(self, command: str):
        """
        Dispatch a command through the registered application services.
        """
        return self._registry.execute(command)