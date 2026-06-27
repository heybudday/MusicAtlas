from datetime import datetime, UTC

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.services.external_identity_service import (
    ExternalIdentityService,
)


def create_session():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    return Session()


def test_create_find_and_upsert():
    session = create_session()

    service = ExternalIdentityService(session)

    # Create

    created = service.create(
        entity_type="artist",
        entity_key="artist:jeff_mills",
        service="spotify",
        external_id="12345",
        external_url="https://open.spotify.com/artist/12345",
        confidence=1.0,
        source="unit_test",
    )

    assert created.external_id == "12345"

    # Find

    found = service.find(
        entity_type="artist",
        entity_key="artist:jeff_mills",
        service="spotify",
    )

    assert found is not None
    assert found.external_id == "12345"

    # Upsert should update existing record

    updated = service.upsert(
        entity_type="artist",
        entity_key="artist:jeff_mills",
        service="spotify",
        external_id="67890",
        external_url="https://open.spotify.com/artist/67890",
        confidence=0.95,
        source="updated_test",
    )

    assert updated.external_id == "67890"
    assert updated.confidence == 0.95

    # Ensure only one record exists

    found_again = service.find(
        entity_type="artist",
        entity_key="artist:jeff_mills",
        service="spotify",
    )

    assert found_again.external_id == "67890"
    assert found_again.source == "updated_test"