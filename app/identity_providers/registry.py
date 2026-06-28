from app.identity_providers.discogs import DiscogsProvider
from app.identity_providers.musicbrainz import MusicBrainzProvider
from app.identity_providers.spotify import SpotifyProvider


class DummyClient:
    pass


class IdentityProviderRegistry:
    def __init__(self, providers=None):
        self.providers = providers or {}

    def register(self, name, provider):
        self.providers[name] = provider

    def get(self, name):
        return self.providers.get(name)

    def service_names(self):
        return list(self.providers.keys())


def create_default_registry():
    registry = IdentityProviderRegistry()

    registry.register("discogs", DiscogsProvider())
    registry.register("musicbrainz", MusicBrainzProvider(client=DummyClient()))
    registry.register("spotify", SpotifyProvider())

    return registry