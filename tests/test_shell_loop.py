from app.application import Application
from app.desktop.desktop_shell import DesktopShell


def test_shell_run_exits_after_exit_command():
    app = Application.create()

    shell = DesktopShell(app)

    inputs = iter(["exit"])

    output = []

    result = shell.run(
        input_func=lambda _: next(inputs),
        output_func=output.append,
    )

    assert result is True
    assert output == []