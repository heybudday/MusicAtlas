from __future__ import annotations


class IdentityAuditRunner:
    """
    Runs identity audits across a batch of artist queries.

    The runner executes each lookup independently so that a failure
    for one artist does not stop the remainder of the batch.
    """

    def __init__(self, audit_service):
        self.audit_service = audit_service

    def audit_artists(self, artists):
        results = []

        for artist in artists:
            try:
                report = self.audit_service.audit_artist(artist)

                results.append(
                    {
                        "query": artist,
                        **report,
                    }
                )

            except Exception as exc:
                results.append(
                    {
                        "query": artist,
                        "matched": False,
                        "error": str(exc),
                    }
                )

        return results