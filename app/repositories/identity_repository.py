from sqlalchemy import select

from app.models.external_identity import ExternalIdentity
from app.models.review_queue import ReviewQueue
from app.models.unresolved_artist import UnresolvedArtist
from app.models.unresolved_label import UnresolvedLabel
from app.repositories.base_repository import BaseRepository


class IdentityRepository(BaseRepository):
    """Repository for identity resolution and review queue operations."""

    def lookup_artist(self, artist_key: str) -> ExternalIdentity | None:
        stmt = (
            select(ExternalIdentity)
            .where(ExternalIdentity.local_key == artist_key)
            .limit(1)
        )
        return self.session.scalar(stmt)

    def lookup_label(self, label_key: str) -> ExternalIdentity | None:
        stmt = (
            select(ExternalIdentity)
            .where(ExternalIdentity.local_key == label_key)
            .limit(1)
        )
        return self.session.scalar(stmt)

    def find_unresolved_artist(self, artist_key: str) -> UnresolvedArtist | None:
        stmt = (
            select(UnresolvedArtist)
            .where(UnresolvedArtist.artist_key == artist_key)
            .limit(1)
        )
        return self.session.scalar(stmt)

    def find_unresolved_label(self, label_key: str) -> UnresolvedLabel | None:
        stmt = (
            select(UnresolvedLabel)
            .where(UnresolvedLabel.label_key == label_key)
            .limit(1)
        )
        return self.session.scalar(stmt)

    def get_pending_reviews(self) -> list[ReviewQueue]:
        stmt = (
            select(ReviewQueue)
            .where(ReviewQueue.status == "pending")
            .order_by(ReviewQueue.created_at)
        )
        return list(self.session.scalars(stmt))