from sqlalchemy import select

from app.models.artist import Artist
from app.repositories.base_repository import BaseRepository


class ArtistRepository(BaseRepository):
    """Repository for Artist queries."""

    def find_by_normalized_name(self, normalized_name: str) -> Artist | None:
        stmt = (
            select(Artist)
            .where(Artist.normalized_name == normalized_name)
            .limit(1)
        )

        return self.session.scalar(stmt)