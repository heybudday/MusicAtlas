from sqlalchemy import ForeignKey, Integer, Text, Index, cast, literal, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.models.artist import Artist
from app.models.base import Base
from app.models.unresolved_artist import UnresolvedArtist


class ReleaseArtist(Base):
    __tablename__ = "release_artists"

    discogs_release_id: Mapped[int] = mapped_column(
        ForeignKey("releases.discogs_release_id"),
        primary_key=True,
    )
    artist_key: Mapped[str] = mapped_column(Text, primary_key=True)
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

    resolved_artist = relationship(
        "Artist",
        primaryjoin=lambda: or_(
            foreign(ReleaseArtist.artist_key) == cast(Artist.discogs_artist_id, Text),
            foreign(ReleaseArtist.artist_key)
            == literal("artist:") + cast(Artist.discogs_artist_id, Text),
        ),
        viewonly=True,
        uselist=False,
    )

    unresolved_artist = relationship(
        "UnresolvedArtist",
        primaryjoin=lambda: foreign(ReleaseArtist.artist_key)
        == UnresolvedArtist.unresolved_artist_key,
        viewonly=True,
        uselist=False,
    )

    @property
    def artist(self):
        return self.resolved_artist or self.unresolved_artist

    __table_args__ = (
        Index("idx_release_artists_artist_key", "artist_key"),
    )