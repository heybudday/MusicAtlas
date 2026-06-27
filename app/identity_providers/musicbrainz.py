from __future__ import annotations

from app.clients.musicbrainz import MusicBrainzClient
from app.identity_providers.base import IdentityProvider


class MusicBrainzProvider(IdentityProvider):
    """
    Identity provider implementation for MusicBrainz.
    """

    def __init__(self, client=None):
        self.client = client or MusicBrainzClient()

    def lookup_artist(self, identifier):
        result = self.client.search_artist(identifier)

        if result is None:
            return {
                "matched": False,
                "external_id": None,
                "url": None,
                "confidence": 0.0,
                "reason": "musicbrainz_artist_not_found",
            }

        confidence = result["score"] / 100

        return {
            "matched": True,
            "external_id": result["id"],
            "url": f"https://musicbrainz.org/artist/{result['id']}",
            "confidence": confidence,
            "reason": "musicbrainz_artist_match",
        }

    def lookup_label(self, identifier):
        result = self.client.search_label(identifier)

        if result is None:
            return {
                "matched": False,
                "external_id": None,
                "url": None,
                "confidence": 0.0,
                "reason": "musicbrainz_label_not_found",
            }

        confidence = result["score"] / 100

        return {
            "matched": True,
            "external_id": result["id"],
            "url": f"https://musicbrainz.org/label/{result['id']}",
            "confidence": confidence,
            "reason": "musicbrainz_label_match",
        }

    def lookup_release(self, identifier):
        raise NotImplementedError