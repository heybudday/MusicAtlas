from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.release import Release
from app.models.release_artist import ReleaseArtist
from app.models.release_label import ReleaseLabel
from app.models.track import Track
from app.models.track_artist import TrackArtist


def get_release_by_id(session: Session, discogs_release_id: int) -> Release | None:
    return session.get(Release, discogs_release_id)


def get_release_graph(session: Session, discogs_release_id: int) -> Release | None:
    stmt = (
        select(Release)
        .where(Release.discogs_release_id == discogs_release_id)
        .options(
            selectinload(Release.release_artists),
            selectinload(Release.release_labels),
            selectinload(Release.tracks).selectinload(Track.track_artists),
        )
    )

    return session.scalar(stmt)


def get_releases_for_artist_key(
    session: Session,
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

    return list(session.scalars(stmt))


def get_releases_for_label_key(
    session: Session,
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

    return list(session.scalars(stmt))


def get_releases_with_track_artist_key(
    session: Session,
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

    return list(session.scalars(stmt))