from app.application import Application


def test_help_groups_commands_by_category():
    app = Application.create()

    result = app.shell.run_once("help")

    assert result == (
        "General\n"
        "-------\n"
        "hello\n"
        "help\n"
        "\n"
        "File\n"
        "----\n"
        "open\n"
        "\n"
        "System\n"
        "------\n"
        "exit"
    )