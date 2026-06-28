from pathlib import Path


class ReportArchiveLoader:
    """
    Loads previously archived report files from disk.
    """

    def __init__(self, archive_directory):
        self.archive_directory = Path(archive_directory)

    def load(self, filename):
        path = self.archive_directory / filename

        if not path.exists():
            raise FileNotFoundError(f"Archived report not found: {filename}")

        return path.read_text()