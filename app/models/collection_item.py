from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class CollectionItem(Base):
    __tablename__ = "collection_items"

    discogs_release_id: Mapped[int] = mapped_column(
        ForeignKey("releases.discogs_release_id"),
        primary_key=True,
    )
    collection_folder: Mapped[str] = mapped_column(Text, nullable=True)
    date_added: Mapped[str] = mapped_column(Text, nullable=True)
    media_condition: Mapped[str] = mapped_column(Text, nullable=True)
    sleeve_condition: Mapped[str] = mapped_column(Text, nullable=True)
    collection_notes: Mapped[str] = mapped_column(Text, nullable=True)
    rating: Mapped[str] = mapped_column(Text, nullable=True)
    imported_at: Mapped[str] = mapped_column(Text, nullable=False)

    release = relationship("Release", back_populates="collection_item")