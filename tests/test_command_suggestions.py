from app.application import Application
from app.ui.command_suggestions import CommandSuggestions


def test_command_suggestions():
    app = Application.create()

    suggestions = CommandSuggestions(app.services.command_registry)

    assert suggestions.suggest("halp") == ["help"]
    assert suggestions.suggest("helo") == ["hello"]
    assert suggestions.suggest("exot") == ["exit"]
    assert suggestions.suggest("xyz") == []