from app.ui.command import Command
from app.ui.command_registry import CommandRegistry


def test_registry_can_lookup_command_by_name():
    registry = CommandRegistry()

    hello = Command(
        name="hello",
        execute=lambda: "hello",
    )

    registry.register(hello)

    assert registry.get("hello") is hello


def test_registry_lookup_returns_none_for_unknown_command():
    registry = CommandRegistry()

    assert registry.get("unknown") is None


def test_registry_lookup_is_case_insensitive():
    registry = CommandRegistry()

    hello = Command(
        name="hello",
        execute=lambda: "hello",
    )

    registry.register(hello)

    assert registry.get("HELLO") is hello
    assert registry.get("Hello") is hello
    assert registry.get("hElLo") is hello