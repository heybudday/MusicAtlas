from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.models.base import Base


class IdentityReview(Base):
    __tablename__ = "identity_review_queue"

    id = Column(Integer, primary_key=True)

    entity_type = Column(String(50))
    entity_key = Column(String(255))

    provider = Column(String(50))

    candidate_external_id = Column(String(255))
    candidate_name = Column(String(255))

    confidence = Column(Float)

    reason = Column(String(255))

    status = Column(String(50))

    review_notes = Column(String(1000))

    created_at = Column(DateTime, default=datetime.utcnow)

    reviewed_at = Column(DateTime, nullable=True)