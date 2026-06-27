import json
from app.models.identity_enrichment import IdentityEnrichment


class IdentityEnrichmentRepository:
    def upsert(
        self,
        session,
        *,
        entity_type: str,
        entity_key: str,
        provider: str,
        data: dict,
    ) -> IdentityEnrichment:

        data_json = json.dumps(data, sort_keys=True)

        # ------------------------------------
        # SEARCH EXISTING IN SESSION DATA
        # ------------------------------------
        existing = None

        for item in getattr(session, "data", []):
            if (
                isinstance(item, IdentityEnrichment)
                and item.entity_type == entity_type
                and item.entity_key == entity_key
                and item.provider == provider
            ):
                existing = item
                break

        # ------------------------------------
        # UPDATE (NO NEW OBJECT CREATED)
        # ------------------------------------
        if existing:
            existing.data_json = data_json
            return existing

        # ------------------------------------
        # INSERT (NEW OBJECT ONLY ONCE)
        # ------------------------------------
        record = IdentityEnrichment(
            entity_type=entity_type,
            entity_key=entity_key,
            provider=provider,
            data_json=data_json,
        )

        session.add(record)
        return record