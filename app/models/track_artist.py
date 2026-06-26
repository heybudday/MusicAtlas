from sqlalchemy import ForeignKeyConstraint, Text, cast, literal, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.models.artist import Artist
from app.models.base import Base
from app.models.unresolved_artist import UnresolvedArtist


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

    resolved_artist = relationship(
        "Artist",
        primaryjoin=lambda: or_(
            foreign(TrackArtist.artist_key) == cast(Artist.discogs_artist_id, Text),
            foreign(TrackArtist.artist_key)
            == literal("artist:") + cast(Artist.discogs_artist_id, Text),
        ),
        viewonly=True,
        uselist=False,
    )

    unresolved_artist = relationship(
        "UnresolvedArtist",
        primaryjoin=lambda: foreign(TrackArtist.artist_key)
        == UnresolvedArtist.unresolved_artist_key,
        viewonly=True,
        uselist=False,
    )

    @property
    def artist(self):
        return self.resolved_artist or self.unresolved_artist

    __table_args__ = (
        ForeignKeyConstraint(
            ["discogs_release_id", "track_position"],
            ["tracks.discogs_release_id", "tracks.track_position"],
        ),
    )