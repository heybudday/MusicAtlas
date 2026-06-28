from app.services.service_registry import ServiceRegistry


class DummyService:
    pass


def test_returns_registered_service():
    service = DummyService()

    registry = ServiceRegistry(
        archive_service=service,
    )

    assert registry.get("archive_service") is service


def test_available_services_are_sorted():
    registry = ServiceRegistry(
        search_service=DummyService(),
        archive_service=DummyService(),
        delete_service=DummyService(),
    )

    assert registry.available_services() == [
        "archive_service",
        "delete_service",
        "search_service",
    ]


def test_unknown_service_raises_key_error():
    registry = ServiceRegistry()

    try:
        registry.get("missing")
        assert False
    except KeyError:
        pass


def test_none_services_not_reported():
    registry = ServiceRegistry(
        archive_service=DummyService(),
        history_service=None,
    )

    assert registry.available_services() == [
        "archive_service",
    ]