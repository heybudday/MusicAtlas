from sqlalchemy import ForeignKey, Integer, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ReleaseLabel(Base):
    __tablename__ = "release_labels"

    discogs_release_id: Mapped[int] = mapped_column(
        ForeignKey("releases.discogs_release_id"),
        primary_key=True,
    )
    label_key: Mapped[str] = mapped_column(Text, primary_key=True)
    position: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        default=0,
    )
    source: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="csv_label_field",
    )

    release = relationship("Release", back_populates="release_labels")

    __table_args__ = (
        Index("idx_release_labels_label_key", "label_key"),
    )