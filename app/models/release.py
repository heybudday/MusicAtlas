from __future__ import annotations

from typing import Optional

from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Release(Base):
    __tablename__ = "releases"

    discogs_release_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(Text)
    released_year: Mapped[Optional[int]] = mapped_column(Integer)
    catalog_number: Mapped[Optional[str]] = mapped_column(Text)
    format: Mapped[Optional[str]] = mapped_column(Text)
    raw_artist: Mapped[Optional[str]] = mapped_column(Text)
    raw_label: Mapped[Optional[str]] = mapped_column(Text)
    imported_at: Mapped[str] = mapped_column(Text, nullable=False)