from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Base repository providing common CRUD operations.
    """

    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def get_by_id(self, obj_id: int) -> T | None:
        return self.session.get(self.model, obj_id)

    def list_all(self) -> list[T]:
        stmt = select(self.model)
        return list(self.session.scalars(stmt))

    def add(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: T) -> None:
        self.session.delete(obj)
        self.session.commit()

    def save(self) -> None:
        """
        Commit pending changes.
        """
        self.session.commit()