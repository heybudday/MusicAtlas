from sqlalchemy import select

from app.models.artist import Artist


def find_by_normalized_name(session, normalized_name: str):
    stmt = (
        select(Artist)
        .where(Artist.normalized_name == normalized_name)
        .limit(1)
    )

    return session.scalar(stmt)