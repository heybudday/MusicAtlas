from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.label import Label
from app.repositories.base_repository import BaseRepository


class LabelRepository(BaseRepository[Label]):
    model = Label

    def __init__(self, session: Session):
        super().__init__(session, self.model)

    def find_by_name(self, name: str) -> Label | None:
        stmt = select(Label).where(Label.name == name)
        return self.session.scalar(stmt)

    def search(self, text: str) -> list[Label]:
        stmt = (
            select(Label)
            .where(Label.name.ilike(f"%{text}%"))
            .order_by(Label.name)
        )
        return list(self.session.scalars(stmt))