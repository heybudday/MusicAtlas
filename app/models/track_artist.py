from sqlalchemy import ForeignKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TrackArtist(Base):
    __tablename__ = "track_artists"

    discogs_release_id: Mapped[int] = mapped_column(primary_key=True)
    track_position: Mapped[str] = mapped_column(Text, primary_key=True)
    artist_key: Mapped[str] = mapped_column(Text, primary_key=True)
    role: Mapped[str] = mapped_column(
        Text,
        primary_key=True,
        nullable=False,
        default="track_artist",
    )
    source: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="discogs_api_pending",
    )

    track = relationship("Track", back_populates="track_artists")

    __table_args__ = (
        ForeignKeyConstraint(
            ["discogs_release_id", "track_position"],
            ["tracks.discogs_release_id", "tracks.track_position"],
        ),
    )