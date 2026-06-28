from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    """
    Base class for UI commands.

    Commands provide a small, consistent interface for actions that can be
    triggered by desktop, mobile, CLI, or other front ends.
    """

    @abstractmethod
    def execute(self) -> Any:
        """
        Execute the command.
        """
        raise NotImplementedError