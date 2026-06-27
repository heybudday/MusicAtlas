import json

from app.models.base import Base
from app.models.identity_enrichment import IdentityEnrichment
from app.repositories.identity_enrichment_repository import IdentityEnrichmentRepository


def test_identity_enrichment_upsert(db_session):
    Base.metadata.create_all(db_session.get_bind())

    repo = IdentityEnrichmentRepository()

    record = repo.upsert(
        db_session,
        entity_type="artist",
        entity_key="123",
        provider="musicbrainz",
        data={"name": "Jeff Mills", "type": "Person"},
    )

    db_session.commit()

    assert record.entity_type == "artist"
    assert record.entity_key == "123"
    assert record.provider == "musicbrainz"
    assert json.loads(record.data_json) == {
        "name": "Jeff Mills",
        "type": "Person",
    }

    updated = repo.upsert(
        db_session,
        entity_type="artist",
        entity_key="123",
        provider="musicbrainz",
        data={"name": "Jeff Mills", "country": "US"},
    )

    db_session.commit()

    rows = db_session.query(IdentityEnrichment).all()

    assert len(rows) == 1
    assert updated.entity_type == "artist"
    assert json.loads(updated.data_json) == {
        "country": "US",
        "name": "Jeff Mills",
    }