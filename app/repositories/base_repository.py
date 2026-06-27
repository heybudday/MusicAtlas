from sqlalchemy.orm import Session


class BaseRepository:
    """Base class for all repositories."""

    def __init__(self, session: Session):
        self.session = session

    def add(self, obj):
        self.session.add(obj)
        return obj

    def delete(self, obj):
        self.session.delete(obj)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def refresh(self, obj):
        self.session.refresh(obj)