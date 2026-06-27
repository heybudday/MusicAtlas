from sqlalchemy import select

from app.models.track import Track
from app.repositories.base_repository import BaseRepository


class TrackRepository(BaseRepository):
    """Repository for Track queries."""

    def get_tracks_for_release(
        self,
        discogs_release_id: int,
    ) -> list[Track]:
        stmt = (
            select(Track)
            .where(Track.discogs_release_id == discogs_release_id)
            .order_by(Track.track_position)
        )

        return list(self.session.scalars(stmt))