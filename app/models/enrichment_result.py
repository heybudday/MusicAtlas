from dataclasses import dataclass
from typing import Any


@dataclass
class EnrichmentResult:
    provider: str
    success: bool
    data: dict[str, Any]
    errors: list[str]