from app.application import Application
from app.desktop.desktop_shell import DesktopShell


def test_shell_exit_command():
    app = Application.create()

    shell = DesktopShell(app)

    assert shell.process_input("exit") is False