from app.application import Application
from app.desktop.desktop_shell import DesktopShell


def test_shell_processes_input():
    app = Application.create()

    shell = DesktopShell(app)

    assert shell.process_input("hello") == "hello"