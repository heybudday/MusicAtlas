from app.reporting.report_writer import ReportWriter


def test_report_writer_creates_file(tmp_path):
    writer = ReportWriter(output_directory=tmp_path)

    path = writer.write("test.txt", "hello")

    assert path.exists()
    assert path.read_text() == "hello"