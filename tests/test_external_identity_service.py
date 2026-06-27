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
        confidence=1.0,
        reason="exact_name_match",
        source="unit_test",
    )

    assert created.external_id == "12345"
    assert created.confidence == 1.0
    assert created.reason == "exact_name_match"

    # Find

    found = service.find(
        entity_type="artist",
        entity_key="artist:jeff_mills",
        service="spotify",
    )

    assert found is not None
    assert found.external_id == "12345"
    assert found.confidence == 1.0
    assert found.reason == "exact_name_match"

    # Upsert should update existing record

    updated = service.upsert(
        entity_type="artist",
        entity_key="artist:jeff_mills",
        service="spotify",
        external_id="67890",
        confidence=0.95,
        reason="best_available_match",
        source="updated_test",
    )

    assert updated.external_id == "67890"
    assert updated.confidence == 0.95
    assert updated.reason == "best_available_match"

    # Ensure only one record exists

    found_again = service.find(
        entity_type="artist",
        entity_key="artist:jeff_mills",
        service="spotify",
    )

    assert found_again.external_id == "67890"
    assert found_again.confidence == 0.95
    assert found_again.reason == "best_available_match"
    assert found_again.source == "updated_test"