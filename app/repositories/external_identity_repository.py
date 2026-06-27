from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.external_identity import ExternalIdentity


class ExternalIdentityRepository:
    def __init__(self, session: Session):
        self.session = session

    def find(
        self,
        entity_type: str,
        entity_key: str,
        service: str,
    ) -> ExternalIdentity | None:
        stmt = (
            select(ExternalIdentity)
            .where(ExternalIdentity.entity_type == entity_type)
            .where(ExternalIdentity.entity_key == entity_key)
            .where(ExternalIdentity.service == service)
        )

        return self.session.scalar(stmt)

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
    ) -> ExternalIdentity:
        identity = ExternalIdentity(
            entity_type=entity_type,
            entity_key=entity_key,
            service=service,
            external_id=external_id,
            url=external_url,
            confidence=confidence,
            reason=reason,
            source=source,
        )

        self.session.add(identity)
        self.session.commit()

        return identity