from sqlalchemy.orm import Session

from app.repositories.external_identity_repository import (
    ExternalIdentityRepository,
)


class ExternalIdentityService:
    def __init__(self, session: Session):
        self.repository = ExternalIdentityRepository(session)

    def find(
        self,
        entity_type: str,
        entity_key: str,
        service: str,
    ):
        return self.repository.find(
            entity_type=entity_type,
            entity_key=entity_key,
            service=service,
        )

    def create(
        self,
        entity_type: str,
        entity_key: str,
        service: str,
        external_id: str,
        external_url: str | None = None,
        confidence: float = 1.0,
        source: str = "manual",
    ):
        return self.repository.create(
            entity_type=entity_type,
            entity_key=entity_key,
            service=service,
            external_id=external_id,
            external_url=external_url,
            confidence=confidence,
            source=source,
        )

    def upsert(
        self,
        entity_type: str,
        entity_key: str,
        service: str,
        external_id: str,
        external_url: str | None = None,
        confidence: float = 1.0,
        source: str = "manual",
    ):
        existing = self.find(
            entity_type,
            entity_key,
            service,
        )

        if existing:
            existing.external_id = external_id
            existing.external_url = external_url
            existing.confidence = confidence
            existing.source = source

            self.repository.session.commit()
            return existing

        return self.create(
            entity_type,
            entity_key,
            service,
            external_id,
            external_url,
            confidence,
            source,
        )