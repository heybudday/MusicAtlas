from app.repositories import artist_repository, label_repository


def normalize_name(name: str) -> str:
    """
    Normalize a name for lookup.

    This implementation matches the current normalization used in the
    Music Atlas database: lowercase and trim leading/trailing whitespace.
    """
    return name.lower().strip()


class IdentityResolver:
    def __init__(self, session):
        self.session = session

    def find_matching_artist(self, raw_name: str):
        normalized = normalize_name(raw_name)

        artist = artist_repository.find_by_normalized_name(
            self.session,
            normalized,
        )

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

    def find_matching_label(self, raw_name: str):
        normalized = normalize_name(raw_name)

        label = label_repository.find_by_normalized_name(
            self.session,
            normalized,
        )

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