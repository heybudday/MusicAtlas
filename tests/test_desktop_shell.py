from app.application import Application
from app.desktop.desktop_shell import DesktopShell
from app.services.service_registry import ServiceRegistry


def test_shell_can_be_created():
    app = Application.create()

    shell = DesktopShell(app)

    assert shell is not None


def test_shell_exposes_application():
    app = Application.create()

    shell = DesktopShell(app)

    assert shell.application is app


def test_shell_exposes_service_registry():
    app = Application.create()

    shell = DesktopShell(app)

    assert isinstance(shell.services, ServiceRegistry)
    assert shell.services is app.services


def test_shell_exposes_application_dispatcher():
    app = Application.create()

    shell = DesktopShell(app)

    assert shell.dispatcher is app.dispatcher


def test_run_returns_success():
    app = Application.create()

    shell = DesktopShell(app)

    assert shell.run() is True