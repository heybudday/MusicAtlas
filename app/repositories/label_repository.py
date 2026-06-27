from sqlalchemy import select

from app.models.label import Label


def find_by_normalized_name(session, normalized_name: str):
    stmt = (
        select(Label)
        .where(Label.normalized_name == normalized_name)
        .limit(1)
    )

    return session.scalar(stmt)