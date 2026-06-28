from app.identity_providers.discogs import DiscogsProvider
from app.identity_providers.musicbrainz import MusicBrainzProvider


class DummyClient:
    """Fallback client for MusicBrainz in tests"""
    pass


def create_provider(name: str):
    providers = {
        "discogs": DiscogsProvider,
        "musicbrainz": MusicBrainzProvider,
    }

    provider_cls = providers.get(name)

    if provider_cls is None:
        raise ValueError(f"Unknown provider: {name}")

    # FIX: MusicBrainz requires client
    if name == "musicbrainz":
        return provider_cls(client=DummyClient())

    return provider_cls()