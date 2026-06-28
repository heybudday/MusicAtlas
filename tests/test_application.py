from app.application import Application
from app.services.service_registry import ServiceRegistry


def test_application_creates_service_registry():
    app = Application()

    assert isinstance(app.services, ServiceRegistry)


def test_create_factory_returns_application():
    app = Application.create()

    assert isinstance(app, Application)
    assert isinstance(app.services, ServiceRegistry)


def test_service_registry_is_shared():
    app = Application()

    assert app.services is app.services