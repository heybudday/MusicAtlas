from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.release import Release
from app.models.release_artist import ReleaseArtist
from app.models.release_label import ReleaseLabel
from app.models.track import Track
from app.models.track_artist import TrackArtist
from app.repositories.base_repository import BaseRepository


class ReleaseRepository(BaseRepository):
    """Repository for Release queries."""

    def get_release_by_id(self, discogs_release_id: int) -> Release | None:
        return self.session.get(Release, discogs_release_id)

    def get_release_graph(self, discogs_release_id: int) -> Release | None:
        stmt = (
            select(Release)
            .where(Release.discogs_release_id == discogs_release_id)
            .options(
                selectinload(Release.release_artists),
                selectinload(Release.release_labels),
                selectinload(Release.tracks).selectinload(Track.track_artists),
            )
        )

        return self.session.scalar(stmt)

    def get_releases_for_artist_key(
        self,
        artist_key: str,
        limit: int = 25,
    ) -> list[Release]:
        stmt = (
            select(Release)
            .join(ReleaseArtist)
            .where(ReleaseArtist.artist_key == artist_key)
            .order_by(Release.released_year, Release.title)
            .limit(limit)
        )

        return list(self.session.scalars(stmt))

    def get_releases_for_label_key(
        self,
        label_key: str,
        limit: int = 25,
    ) -> list[Release]:
        stmt = (
            select(Release)
            .join(ReleaseLabel)
            .where(ReleaseLabel.label_key == label_key)
            .order_by(Release.released_year, Release.title)
            .limit(limit)
        )

        return list(self.session.scalars(stmt))

    def get_releases_with_track_artist_key(
        self,
        artist_key: str,
        limit: int = 25,
    ) -> list[Release]:
        stmt = (
            select(Release)
            .join(Track)
            .join(TrackArtist)
            .where(TrackArtist.artist_key == artist_key)
            .order_by(Release.released_year, Release.title)
            .distinct()
            .limit(limit)
        )

        return list(self.session.scalars(stmt))