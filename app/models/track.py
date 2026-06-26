from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Track(Base):
    __tablename__ = "tracks"

    discogs_release_id: Mapped[int] = mapped_column(
        ForeignKey("releases.discogs_release_id"),
        primary_key=True,
    )
    track_position: Mapped[str] = mapped_column(Text, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=True)
    duration: Mapped[str] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="discogs_api_pending",
    )

    release = relationship("Release", back_populates="tracks")
    track_artists = relationship("TrackArtist", back_populates="track")