from __future__ import annotations


class IdentityEvidenceCollector:
    EVIDENCE_FIELDS = [
        "website",
        "spotify",
        "discogs",
        "musicbrainz",
        "bandcamp",
        "soundcloud",
        "facebook",
        "instagram",
        "twitter",
        "youtube",
        "tiktok",
    ]

    def collect(self, provider: str, result: dict) -> dict:
        evidence = {
            field: result.get(field)
            for field in self.EVIDENCE_FIELDS
        }

        evidence["sources"] = self._build_sources(
            provider=provider,
            evidence=evidence,
        )

        return evidence

    def _build_sources(self, provider: str, evidence: dict) -> list[dict]:
        sources = []

        for field in self.EVIDENCE_FIELDS:
            if evidence.get(field):
                sources.append(
                    {
                        "field": field,
                        "provider": provider,
                        "confidence": 1.0,
                    }
                )

        return sources