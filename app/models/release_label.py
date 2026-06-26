from sqlalchemy import ForeignKey, Integer, Text, Index, cast, literal, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.models.base import Base
from app.models.label import Label
from app.models.unresolved_label import UnresolvedLabel


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

    resolved_label = relationship(
        "Label",
        primaryjoin=lambda: or_(
            foreign(ReleaseLabel.label_key) == cast(Label.discogs_label_id, Text),
            foreign(ReleaseLabel.label_key)
            == literal("label:") + cast(Label.discogs_label_id, Text),
        ),
        viewonly=True,
        uselist=False,
    )

    unresolved_label = relationship(
        "UnresolvedLabel",
        primaryjoin=lambda: foreign(ReleaseLabel.label_key)
        == UnresolvedLabel.unresolved_label_key,
        viewonly=True,
        uselist=False,
    )

    @property
    def label(self):
        return self.resolved_label or self.unresolved_label

    __table_args__ = (
        Index("idx_release_labels_label_key", "label_key"),
    )