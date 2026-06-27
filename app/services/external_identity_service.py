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
        reason: str | None = None,
        source: str = "manual",
    ):
        return self.repository.create(
            entity_type=entity_type,
            entity_key=entity_key,
            service=service,
            external_id=external_id,
            external_url=external_url,
            confidence=confidence,
            reason=reason,
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
        reason: str | None = None,
        source: str = "manual",
    ):
        existing = self.find(
            entity_type,
            entity_key,
            service,
        )

        if existing:
            existing.external_id = external_id
            existing.url = external_url
            existing.confidence = confidence
            existing.reason = reason
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
            reason,
            source,
        )

    def upsert_artist_identity(
        self,
        artist: str,
        best_match: dict,
    ):
        result = best_match.get("result", {})

        return self.upsert(
            entity_type="artist",
            entity_key=artist,
            service=best_match.get("provider"),
            external_id=result.get("external_id"),
            external_url=result.get("url"),
            confidence=best_match.get("confidence"),
            reason=best_match.get("reason"),
            source="identity_orchestrator",
        )

    def upsert_label_identity(
        self,
        label: str,
        best_match: dict,
    ):
        result = best_match.get("result", {})

        return self.upsert(
            entity_type="label",
            entity_key=label,
            service=best_match.get("provider"),
            external_id=result.get("external_id"),
            external_url=result.get("url"),
            confidence=best_match.get("confidence"),
            reason=best_match.get("reason"),
            source="identity_orchestrator",
        )