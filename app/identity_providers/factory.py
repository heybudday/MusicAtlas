from __future__ import annotations

from app.identity_providers.discogs import DiscogsProvider
from app.identity_providers.musicbrainz import MusicBrainzProvider


def create_provider(name: str):
    """
    Create an identity provider instance.
    """

    providers = {
        "discogs": DiscogsProvider,
        "musicbrainz": MusicBrainzProvider,
    }

    provider_cls = providers.get(name)

    if provider_cls is None:
        raise ValueError(f"Unknown provider: {name}")

    return provider_cls()