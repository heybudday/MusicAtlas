class CommandDispatcher:
    def __init__(self, registry):
        self._registry = registry

    def dispatch(self, command_name: str, *args):
        command = self._registry.get(command_name)

        if command is None:
            return f"Unknown command: {command_name}"

        return command.execute(*args)