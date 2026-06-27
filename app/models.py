class IdentityReviewQueue(Base):
    __tablename__ = "identity_review_queue"

    id = Column(Integer, primary_key=True)

    provider = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)

    query = Column(String, nullable=False)
    candidate_name = Column(String)

    confidence = Column(Float)

    reason = Column(String)

    status = Column(
        String,
        nullable=False,
        default="pending",
    )

    notes = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    reviewed_at = Column(DateTime)