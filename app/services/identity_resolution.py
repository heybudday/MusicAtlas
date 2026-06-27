from app.repositories.artist_repository import ArtistRepository
from app.repositories.label_repository import LabelRepository
from app.utils.normalization import normalize_name


def resolve_artist(artist_repository: ArtistRepository, raw_name: str) -> dict:
    """
    Resolve a raw artist name to a known Artist.
    """

    normalized_name = normalize_name(raw_name)

    artist = artist_repository.find_by_normalized_name(normalized_name)

    if artist is None:
        return {
            "matched": False,
            "confidence": 0.0,
            "reason": "no_exact_normalized_name_match",
        }

    return {
        "matched": True,
        "discogs_artist_id": artist.discogs_artist_id,
        "name": artist.name,
        "confidence": 1.0,
        "reason": "exact_normalized_name",
    }


def resolve_label(label_repository: LabelRepository, raw_name: str) -> dict:
    """
    Resolve a raw label name to a known Label.
    """

    normalized_name = normalize_name(raw_name)

    label = label_repository.find_by_normalized_name(normalized_name)

    if label is None:
        return {
            "matched": False,
            "confidence": 0.0,
            "reason": "no_exact_normalized_name_match",
        }

    return {
        "matched": True,
        "discogs_label_id": label.discogs_label_id,
        "name": label.name,
        "confidence": 1.0,
        "reason": "exact_normalized_name",
    }


def resolve_release_artists(session, release) -> list[dict]:
    """
    Resolve every artist attached to a Release.
    """

    artist_repository = ArtistRepository(session)

    results = []

    for release_artist in release.release_artists:
        artist = release_artist.artist

        if artist is None:
            continue

        results.append(
            resolve_artist(
                artist_repository,
                artist.name,
            )
        )

    return results


def resolve_release_labels(session, release) -> list[dict]:
    """
    Resolve every label attached to a Release.
    """

    label_repository = LabelRepository(session)

    results = []

    for release_label in release.release_labels:
        label = release_label.label

        if label is None:
            continue

        results.append(
            resolve_label(
                label_repository,
                label.name,
            )
        )

    return results