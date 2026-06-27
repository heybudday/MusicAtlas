from __future__ import annotations

from app.identity_providers.factory import create_provider


class IdentityOrchestrator:
    """
    Coordinates identity lookups across one or more providers.
    """

    def enrich_artist(self, artist, providers):
        results = []

        for provider_name in providers:
            provider = create_provider(provider_name)

            result = provider.lookup_artist(artist)

            results.append(
                {
                    "provider": provider_name,
                    "result": result,
                }
            )

        return results

    def enrich_label(self, label, providers):
        results = []

        for provider_name in providers:
            provider = create_provider(provider_name)

            result = provider.lookup_label(label)

            results.append(
                {
                    "provider": provider_name,
                    "result": result,
                }
            )

        return results