from app.ui.command_history import CommandHistory


def test_history_starts_empty():
    history = CommandHistory()

    assert history.commands == []


def test_add_stores_commands_in_order():
    history = CommandHistory()

    history.add("hello")
    history.add("open report.json")

    assert history.commands == ["hello", "open report.json"]


def test_commands_returns_copy():
    history = CommandHistory()
    history.add("hello")

    commands = history.commands
    commands.append("open report.json")

    assert history.commands == ["hello"]