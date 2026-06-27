from __future__ import annotations

from abc import ABC, abstractmethod


class IdentityProvider(ABC):
    """
    Base interface implemented by every external identity provider.
    """

    @abstractmethod
    def lookup_artist(self, identifier):
        pass

    @abstractmethod
    def lookup_label(self, identifier):
        pass

    @abstractmethod
    def lookup_release(self, identifier):
        pass