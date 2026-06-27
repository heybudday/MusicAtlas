from app.identity_providers.registry import IdentityProviderRegistry


class IdentityEnrichmentService:
    """
    Coordinates enrichment from external identity providers.
    """

    def __init__(self, registry=None):
        self.registry = registry or IdentityProviderRegistry()

    def enrich_artist(self, artist):
        """
        Placeholder implementation.

        Later this will:
            • resolve Discogs
            • resolve MusicBrainz
            • resolve Spotify
            • update ExternalIdentity table
            • populate metadata
        """
        return artist

    def enrich_label(self, label):
        """
        Placeholder implementation.
        """
        return label