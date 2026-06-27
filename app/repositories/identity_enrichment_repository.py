from datetime import UTC, datetime
import json

from sqlalchemy.orm import Session

from app.models.identity_enrichment import IdentityEnrichment


class IdentityEnrichmentRepository:
    def upsert(
        self,
        session: Session,
        *,
        entity_type: str,
        entity_key: str,
        provider: str,
        data: dict,
    ) -> IdentityEnrichment:
        now = datetime.now(UTC).isoformat()
        data_json = json.dumps(data, sort_keys=True)

        existing = session.get(
            IdentityEnrichment,
            {
                "entity_type": entity_type,
                "entity_key": entity_key,
                "provider": provider,
            },
        )

        if existing is None:
            existing = IdentityEnrichment(
                entity_type=entity_type,
                entity_key=entity_key,
                provider=provider,
                data_json=data_json,
                updated_at=now,
            )
            session.add(existing)
            return existing

        existing.data_json = data_json
        existing.updated_at = now
        return existing