from app.ui.application_shell import ApplicationShell


class FakeRegistry:
    def __init__(self):
        self.called = []

    def execute(self, command):
        self.called.append(command)
        return f"ran {command}"


def test_dispatches_command_to_registry():
    registry = FakeRegistry()
    shell = ApplicationShell(registry)

    result = shell.dispatch("report:list")

    assert result == "ran report:list"
    assert registry.called == ["report:list"]


def test_multiple_commands_are_forwarded():
    registry = FakeRegistry()
    shell = ApplicationShell(registry)

    shell.dispatch("identity:audit")
    shell.dispatch("report:history")

    assert registry.called == [
        "identity:audit",
        "report:history",
    ]


def test_dispatch_returns_underlying_result():
    registry = FakeRegistry()
    shell = ApplicationShell(registry)

    result = shell.dispatch("anything")

    assert isinstance(result, str)
    assert result == "ran anything"