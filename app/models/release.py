from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Release(Base):
    __tablename__ = "releases"

    discogs_release_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=True)
    released_year: Mapped[int] = mapped_column(Integer, nullable=True)
    catalog_number: Mapped[str] = mapped_column(Text, nullable=True)
    format: Mapped[str] = mapped_column(Text, nullable=True)
    raw_artist: Mapped[str] = mapped_column(Text, nullable=True)
    raw_label: Mapped[str] = mapped_column(Text, nullable=True)
    imported_at: Mapped[str] = mapped_column(Text, nullable=False)

    collection_item = relationship(
        "CollectionItem",
        back_populates="release",
        uselist=False,
    )

    release_artists = relationship(
        "ReleaseArtist",
        back_populates="release",
    )

    release_labels = relationship(
        "ReleaseLabel",
        back_populates="release",
    )

    tracks = relationship(
        "Track",
        back_populates="release",
    )