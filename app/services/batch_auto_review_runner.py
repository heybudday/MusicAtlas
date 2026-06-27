from __future__ import annotations

from app.services.automatic_identity_resolution import AutomaticIdentityResolution


class BatchAutoReviewRunner:
    def __init__(self, session=None, automatic_identity_resolution=None):
        self.session = session
        self.automatic_identity_resolution = (
            automatic_identity_resolution
            or AutomaticIdentityResolution(session=session)
        )

    def run(self, artists, limit=None):
        selected_artists = list(artists)

        if limit is not None:
            selected_artists = selected_artists[:limit]

        summary = {
            "processed": 0,
            "resolved": 0,
            "review_required": 0,
            "skipped": 0,
            "failed": 0,
            "failures": [],
        }

        for artist in selected_artists:
            summary["processed"] += 1

            try:
                result = self.automatic_identity_resolution.resolve(artist)
                status = self._status_from_result(result)

                if status == "resolved":
                    summary["resolved"] += 1
                elif status == "review_required":
                    summary["review_required"] += 1
                else:
                    summary["skipped"] += 1

            except Exception as exc:
                summary["failed"] += 1
                summary["failures"].append(
                    {
                        "artist": artist,
                        "error": str(exc),
                    }
                )

        return summary

    def _status_from_result(self, result):
        if result is None:
            return "skipped"

        if isinstance(result, dict):
            return result.get("status", "skipped")

        return getattr(result, "status", "skipped")