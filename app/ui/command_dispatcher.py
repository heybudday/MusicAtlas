from __future__ import annotations


class CommandDispatcher:
    def __init__(self, registry):
        self.registry = registry

    def dispatch(self, name: str, *args):
        command = self.registry.get(name)

        if command is None:
            return f"Unknown command: {name}"

        return command.execute(*args)