from app.services.service_registry import ServiceRegistry
from app.ui.command_registry import CommandRegistry


def test_service_registry_exposes_command_registry():
    services = ServiceRegistry()

    registry = services.command_registry

    assert isinstance(registry, CommandRegistry)


def test_command_registry_is_singleton():
    services = ServiceRegistry()

    assert services.command_registry is services.command_registry