from sqlalchemy import select

from app.models.label import Label
from app.repositories.base_repository import BaseRepository


class LabelRepository(BaseRepository):
    """Repository for Label queries."""

    def find_by_normalized_name(self, normalized_name: str) -> Label | None:
        stmt = (
            select(Label)
            .where(Label.normalized_name == normalized_name)
            .limit(1)
        )

        return self.session.scalar(stmt)