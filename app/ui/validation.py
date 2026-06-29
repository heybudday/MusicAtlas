from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    message: str = ""


class CommandValidator:
    def validate(self, args) -> ValidationResult:
        return ValidationResult(True)


class RequiredArgumentsValidator(CommandValidator):
    def __init__(self, minimum: int):
        self.minimum = minimum

    def validate(self, args) -> ValidationResult:
        if len(args) < self.minimum:
            return ValidationResult(
                valid=False,
                message=f"Expected at least {self.minimum} argument(s).",
            )

        return ValidationResult(True)