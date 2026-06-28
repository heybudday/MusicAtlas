from app.ui.commands.open_command import OpenCommand


class FakeArchiveService:
    def open(self, name: str):
        return f"opened:{name}"


def test_open_command():
    service = FakeArchiveService()

    command = OpenCommand(service)

    assert command.execute("report.json") == "opened:report.json"