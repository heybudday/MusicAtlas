from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.release import Release
from app.repositories.base_repository import BaseRepository


class ReleaseRepository(BaseRepository[Release]):
    model = Release

    def __init__(self, session: Session):
        super().__init__(session, self.model)

    def find_by_title(self, title: str) -> Release | None:
        stmt = select(Release).where(Release.title == title)
        return self.session.scalar(stmt)

    def search_title(self, text: str) -> list[Release]:
        stmt = (
            select(Release)
            .where(Release.title.ilike(f"%{text}%"))
            .order_by(Release.title)
        )
        return list(self.session.scalars(stmt))

    def released_in(self, year: int) -> list[Release]:
        stmt = (
            select(Release)
            .where(Release.released_year == year)
            .order_by(Release.title)
        )
        return list(self.session.scalars(stmt))

    def find_by_catalog_number(self, catalog_number: str) -> list[Release]:
        stmt = (
            select(Release)
            .where(Release.catalog_number == catalog_number)
            .order_by(Release.title)
        )
        return list(self.session.scalars(stmt))

    def find_by_raw_artist(self, artist: str) -> list[Release]:
        stmt = (
            select(Release)
            .where(Release.raw_artist.ilike(f"%{artist}%"))
            .order_by(Release.released_year, Release.title)
        )
        return list(self.session.scalars(stmt))

    def find_by_raw_label(self, label: str) -> list[Release]:
        stmt = (
            select(Release)
            .where(Release.raw_label.ilike(f"%{label}%"))
            .order_by(Release.released_year, Release.title)
        )
        return list(self.session.scalars(stmt))