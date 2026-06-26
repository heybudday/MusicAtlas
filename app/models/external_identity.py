from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ExternalIdentity(Base):
    __tablename__ = "external_identities"

    entity_type: Mapped[str] = mapped_column(Text, primary_key=True)
    entity_key: Mapped[str] = mapped_column(Text, primary_key=True)
    service: Mapped[str] = mapped_column(Text, primary_key=True)

    external_id: Mapped[str] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="unverified")
    confidence: Mapped[int] = mapped_column(Integer, nullable=True)
    source: Mapped[str] = mapped_column(Text, nullable=True)
    last_checked_at: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[str] = mapped_column(Text, nullable=False)
