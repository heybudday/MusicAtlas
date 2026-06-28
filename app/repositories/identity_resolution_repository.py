from __future__ import annotations


class IdentityResolutionRepository:
    """
    Repository for retrieving identity resolution records.

    The repository is intentionally lightweight so it can be backed by
    SQLAlchemy today and expanded later without changing the reporting
    services.
    """

    def __init__(self, session=None):
        self.session = session

    def all(self):
        """
        Return all identity resolution records.

        If no database session has been supplied, return an empty list so
        callers remain usable in tests.
        """
        if self.session is None:
            return []

        # Placeholder until a concrete IdentityResolution model exists.
        # Future milestones can replace this with a SQLAlchemy query.
        return []