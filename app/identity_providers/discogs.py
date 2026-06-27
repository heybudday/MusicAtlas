class DiscogsProvider:
    """
    Test-safe stub implementation of Discogs provider.
    This is NOT a real API client — it is a deterministic fake for tests.
    """

    def lookup_artist(self, identifier: str):
        return {
            "matched": True,
            "name": identifier,
            "external_id": f"discogs-{identifier.lower().replace(' ', '-')}",
            "url": f"https://discogs.com/artist/{identifier}",
            "confidence": 1.0,
            "reason": "discogs_artist_match",
        }

    def lookup_label(self, identifier: str):
        return {
            "matched": True,
            "name": identifier,
            "external_id": f"discogs-label-{identifier.lower().replace(' ', '-')}",
            "url": f"https://discogs.com/label/{identifier}",
            "confidence": 1.0,
            "reason": "discogs_label_match",
        }