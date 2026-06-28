from app.application import Application
from app.desktop.desktop_shell import DesktopShell


def test_open_command_executes_with_argument():
    app = Application.create()
    shell = DesktopShell(app)

    def fake_input(prompt: str) -> str:
        return "open report_123"

    result = shell.process_input(fake_input("> "))

    assert result == "opened: report_123"