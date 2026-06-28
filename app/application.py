from __future__ import annotations

from app.services.service_registry import ServiceRegistry


class Application:
    """
    Application bootstrap.

    Responsible for constructing and exposing shared services through
    a single ServiceRegistry instance.

    Future desktop, mobile, API, and CLI entry points should construct
    one Application and obtain services from it.
    """

    def __init__(self):
        self._registry = ServiceRegistry()

    @property
    def services(self) -> ServiceRegistry:
        return self._registry

    @classmethod
    def create(cls) -> "Application":
        """
        Factory method used by application entry points.
        """
        return cls()