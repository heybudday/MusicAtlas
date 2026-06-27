from __future__ import annotations

from app.identity_providers.base import IdentityProvider


class SpotifyProvider(IdentityProvider):
    """
    Identity provider for Spotify.
    """

    def lookup_artist(self, identifier):
        raise NotImplementedError

    def lookup_label(self, identifier):
        raise NotImplementedError

    def lookup_release(self, identifier):
        raise NotImplementedError