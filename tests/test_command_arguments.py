from app.application import Application


def test_command_arguments_are_passed():
    app = Application.create()
    shell = app.shell

    # simulate user input
    result = shell.run_once("open report.json")

    # open command should receive argument and echo it (or process it)
    assert result == "opened report.json"