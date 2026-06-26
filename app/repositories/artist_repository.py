from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.artist import Artist
from app.repositories.base_repository import BaseRepository


class ArtistRepository(BaseRepository[Artist]):
    model = Artist

    def __init__(self, session: Session):
        super().__init__(session, self.model)

    def find_by_name(self, name: str) -> Artist | None:
        stmt = select(Artist).where(Artist.name == name)
        return self.session.scalar(stmt)

    def search(self, text: str) -> list[Artist]:
        stmt = (
            select(Artist)
            .where(Artist.name.ilike(f"%{text}%"))
            .order_by(Artist.name)
        )
        return list(self.session.scalars(stmt))