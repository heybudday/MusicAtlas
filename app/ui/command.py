from __future__ import annotations


class Command:
    def __init__(
        self,
        name,
        execute,
        description="",
        shortcut=None,
        category="General",
        usage=None,
        aliases=None,
        examples=None,
    ):
        self.name = name
        self.execute = execute
        self.description = description
        self.shortcut = shortcut
        self.category = category
        self.usage = usage
        self.aliases = aliases or []
        self.examples = examples or []