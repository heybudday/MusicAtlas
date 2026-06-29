from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from app.ui.validation import ValidationResult


@dataclass(frozen=True)
class ArgSpec:
    name: str
    type: type = str
    required: bool = True
    default: Any = None


@dataclass(frozen=True)
class FlagSpec:
    name: str
    description: str = ""


@dataclass
class Command:
    name: str
    execute: Callable[..., Any]

    description: str | None = None

    args: list[ArgSpec] = field(default_factory=list)
    flags: list[FlagSpec] = field(default_factory=list)

    aliases: list[str] = field(default_factory=list)
    shortcut: str | None = None
    usage: str | None = None
    validator: Any = None

    def validate(self, *args) -> ValidationResult:
        if self.validator is None:
            return ValidationResult(True)

        return self.validator.validate(args)

    def __call__(self, *args, **kwargs):
        return self.execute(*args, **kwargs)