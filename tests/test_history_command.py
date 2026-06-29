from app.ui.command_history import CommandHistory
from app.ui.commands.history_command import HistoryCommand


def test_history_command_prints_stored_commands():
    history = CommandHistory()

    history.add("hello")
    history.add("open report.json")
    history.add("help")

    command = HistoryCommand(history)

    assert command.execute() == (
        "1  hello\n"
        "2  open report.json\n"
        "3  help"
    )