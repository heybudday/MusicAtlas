from datetime import datetime, UTC

from sqlalchemy import Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


def utc_now_iso() ->str:
    return datetime.now(UTC).isoformat()


class ExternalIdentity(Base):
    __tablename__ = "external_identities"

    entity_type: Mapped[str] = mapped_column(Text, primary_key=True)
    entity_key: Mapped[str] = mapped_column(Text, primary_key=True)
    service: Mapped[str] = mapped_column(Text, primary_key=True)

    external_id: Mapped[str] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="unverified")
    confidence: Mapped[float] = mapped_column(Float, nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(Text, nullable=True)
    last_checked_at: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=utc_now_iso,
    )
    updated_at: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=utc_now_iso,
        onupdate=utc_now_iso,
    )