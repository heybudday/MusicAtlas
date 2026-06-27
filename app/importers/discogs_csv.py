import csv
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from app.database import SessionLocal
from app.models.artist import Artist
from app.models.label import Label
from app.utils.normalization import normalize_name


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
IMPORTS_DIR = DATA_DIR / "imports"


def read_discogs_csv(csv_path: str) -> List[Dict[str, str]]:
    """Read a Discogs collection CSV export."""
    source = Path(csv_path).expanduser().resolve()

    if not source.exists():
        raise FileNotFoundError(f"CSV file not found: {source}")

    with source.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    return rows


def archive_import_file(csv_path: str) -> Path:
    """Copy the original Discogs CSV into data/imports for safekeeping."""
    IMPORTS_DIR.mkdir(parents=True, exist_ok=True)

    source = Path(csv_path).expanduser().resolve()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    destination = IMPORTS_DIR / f"{timestamp}-{source.name}"

    shutil.copy2(source, destination)

    return destination


def summarize_rows(rows: List[Dict[str, str]]) -> Dict[str, int]:
    """Return simple counts from the Discogs CSV rows."""
    release_ids = set()
    artists = set()
    labels = set()

    for row in rows:
        release_id = (
            row.get("release_id")
            or row.get("Release ID")
            or row.get("Release_id")
        )
        artist = row.get("Artist") or row.get("artist")
        label = row.get("Label") or row.get("label")

        if release_id:
            release_ids.add(release_id.strip())

        if artist:
            artists.add(artist.strip())

        if label:
            labels.add(label.strip())

    return {
        "rows": len(rows),
        "unique_releases": len(release_ids),
        "artists": len(artists),
        "labels": len(labels),
    }


def _get_value(row: Dict[str, str], *keys: str) -> str | None:
    for key in keys:
        value = row.get(key)
        if value is not None and value.strip():
            return value.strip()

    return None


def import_artists_and_labels(rows: List[Dict[str, str]]) -> Dict[str, int]:
    """Import unique raw artist and label names into artists and labels tables."""
    session = SessionLocal()

    try:
        now = datetime.now().isoformat(timespec="seconds")

        artist_names = set()
        label_names = set()

        for row in rows:
            artist = _get_value(row, "Artist", "artist")
            label = _get_value(row, "Label", "label")

            if artist:
                artist_names.add(artist)

            if label:
                label_names.add(label)

        existing_artists = {
            artist.normalized_name
            for artist in session.query(Artist).all()
        }

        existing_labels = {
            label.normalized_name
            for label in session.query(Label).all()
        }

        artists_added = 0
        labels_added = 0

        for index, name in enumerate(sorted(artist_names), start=1):
            normalized_name = normalize_name(name)

            if normalized_name not in existing_artists:
                session.add(
                    Artist(
                        discogs_artist_id=index,
                        name=name,
                        normalized_name=normalized_name,
                        created_at=now,
                        updated_at=now,
                    )
                )
                artists_added += 1

        for index, name in enumerate(sorted(label_names), start=1):
            normalized_name = normalize_name(name)

            if normalized_name not in existing_labels:
                session.add(
                    Label(
                        discogs_label_id=index,
                        name=name,
                        normalized_name=normalized_name,
                        created_at=now,
                        updated_at=now,
                    )
                )
                labels_added += 1

        session.commit()

        return {
            "artists_added": artists_added,
            "labels_added": labels_added,
        }

    finally:
        session.close()


def import_discogs_csv(csv_path: str) -> Dict[str, object]:
    """Read, archive, summarize, and import a Discogs CSV export."""
    rows = read_discogs_csv(csv_path)
    archived_path = archive_import_file(csv_path)
    summary = summarize_rows(rows)
    import_summary = import_artists_and_labels(rows)

    return {
        "archived_path": archived_path,
        "summary": summary,
        "import_summary": import_summary,
    }