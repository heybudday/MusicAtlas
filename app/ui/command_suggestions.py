from __future__ import annotations

from difflib import get_close_matches


class CommandSuggestions:
    def __init__(self, registry):
        self.registry = registry

    def suggest(self, text: str) -> list[str]:
        command_names = [command.name for command in self.registry.commands]

        return get_close_matches(
            text,
            command_names,
            n=1,
            cutoff=0.6,
        )