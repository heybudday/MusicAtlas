from __future__ import annotations

from app.identity_providers.base import IdentityProvider


class DiscogsProvider(IdentityProvider):
    """
    Identity provider for Discogs.
    """

    def lookup_artist(self, identifier):
        raise NotImplementedError

    def lookup_label(self, identifier):
        raise NotImplementedError

    def lookup_release(self, identifier):
        raise NotImplementedError