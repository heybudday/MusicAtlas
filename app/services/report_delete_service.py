class ReportDeleteService:
    """
    Service responsible for deleting archived reports.
    """

    def __init__(self, archive):
        self.archive = archive

    def delete_report(self, filename):
        """
        Delete a report by filename.

        Returns:
            True if the report was deleted.
            False if the report did not exist.
        """
        return self.archive.delete_report(filename)