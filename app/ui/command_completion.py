from __future__ import annotations


class CommandCompletion:
    def __init__(self, registry):
        self.registry = registry

    def complete(self, partial: str) -> list[str]:
        query = partial.strip().lower()

        matches = []

        for command in self.registry.commands:
            name = command.name

            if name.lower().startswith(query):
                matches.append(name)
                continue

            for alias in command.aliases:
                if alias.lower().startswith(query):
                    matches.append(name)
                    break

        return sorted(set(matches))