from app.application import Application
from app.desktop.desktop_shell import DesktopShell


def test_shell_executes_registered_command():
    app = Application.create()

    shell = DesktopShell(app)

    assert shell.execute_command("hello") == "hello"