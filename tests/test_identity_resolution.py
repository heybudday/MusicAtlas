from app.database import SessionLocal
from app.repositories.artist_repository import ArtistRepository
from app.repositories.label_repository import LabelRepository
from app.repositories.release_repository import ReleaseRepository
from app.services.identity_resolution import (
    resolve_artist,
    resolve_label,
    resolve_release_artists,
    resolve_release_labels,
)


def main():
    session = SessionLocal()

    try:
        artist_repository = ArtistRepository(session)
        label_repository = LabelRepository(session)
        release_repository = ReleaseRepository(session)

        print("=" * 40)
        print("Artist Lookup")
        print("=" * 40)

        print(resolve_artist(artist_repository, "Jeff Mills"))
        print()
        print(resolve_artist(artist_repository, "The Persuader"))
        print()
        print(resolve_artist(artist_repository, "Definitely Not An Artist"))
        print()

        print("=" * 40)
        print("Label Lookup")
        print("=" * 40)

        print(resolve_label(label_repository, "Svek"))
        print()
        print(resolve_label(label_repository, "Warp Records"))
        print()
        print(resolve_label(label_repository, "Definitely Not A Label"))
        print()

        print("=" * 40)
        print("Release Resolution")
        print("=" * 40)

        release = release_repository.get_release_graph(1)

        if release is None:
            print("Release not found.")
            return

        print("Artists")
        print(resolve_release_artists(session, release))
        print()

        print("Labels")
        print(resolve_release_labels(session, release))

    finally:
        session.close()


if __name__ == "__main__":
    main()