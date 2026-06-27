from app.identity_providers.base import IdentityProvider
from app.identity_providers.discogs import DiscogsProvider
from app.identity_providers.musicbrainz import MusicBrainzProvider
from app.identity_providers.spotify import SpotifyProvider


class IdentityProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, IdentityProvider] = {}

    def register(self, service_name: str, provider: IdentityProvider) -> None:
        self._providers[service_name] = provider

    def get(self, service_name: str) -> IdentityProvider | None:
        return self._providers.get(service_name)

    def all(self) -> list[IdentityProvider]:
        return list(self._providers.values())

    def service_names(self) -> list[str]:
        return list(self._providers.keys())


def create_default_registry() -> IdentityProviderRegistry:
    registry = IdentityProviderRegistry()

    registry.register("discogs", DiscogsProvider())
    registry.register("musicbrainz", MusicBrainzProvider())
    registry.register("spotify", SpotifyProvider())

    return registry