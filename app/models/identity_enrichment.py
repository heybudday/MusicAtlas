from sqlalchemy import Text

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class IdentityEnrichment(Base):
    __tablename__ = "identity_enrichment"

    entity_type: Mapped[str] = mapped_column(Text, primary_key=True)
    entity_key: Mapped[str] = mapped_column(Text, primary_key=True)
    provider: Mapped[str] = mapped_column(Text, primary_key=True)

    data_json: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    updated_at: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )