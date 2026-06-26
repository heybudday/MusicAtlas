from sqlalchemy import ForeignKey, Integer, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ReleaseArtist(Base):
    __tablename__ = "release_artists"

    discogs_release_id: Mapped[int] = mapped_column(
        ForeignKey("releases.discogs_release_id"),
        primary_key=True,
    )
    artist_key: Mapped[str] = mapped_column(
        Text,
        primary_key=True,
    )
    role: Mapped[str] = mapped_column(
        Text,
        primary_key=True,
        nullable=False,
        default="primary_release_artist",
    )
    position: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        default=0,
    )
    source: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="csv_artist_field",
    )

    release = relationship("Release", back_populates="release_artists")

    __table_args__ = (
        Index("idx_release_artists_artist_key", "artist_key"),
    )