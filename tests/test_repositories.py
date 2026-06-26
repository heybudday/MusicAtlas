from app.database import SessionLocal
from app.repositories.artist_repository import ArtistRepository
from app.repositories.label_repository import LabelRepository
from app.repositories.release_repository import ReleaseRepository


def main():
    session = SessionLocal()

    try:
        artist_repo = ArtistRepository(session)
        label_repo = LabelRepository(session)
        release_repo = ReleaseRepository(session)

        release = release_repo.get_by_id(1)

        if release is None:
            print("No release found with Discogs Release ID 1.")
        else:
            print("Release")
            print("-------")
            print(f"Discogs Release ID : {release.discogs_release_id}")
            print(f"Title              : {release.title}")
            print(f"Released Year      : {release.released_year}")
            print(f"Catalog Number     : {release.catalog_number}")
            print(f"Format             : {release.format}")
            print(f"Raw Artist         : {release.raw_artist}")
            print(f"Raw Label          : {release.raw_label}")

        print("\nReleases matching 'Stockholm'")
        print("-----------------------------")
        for item in release_repo.search_title("Stockholm")[:10]:
            print(
                f"{item.discogs_release_id}: "
                f"{item.title} "
                f"({item.released_year})"
            )

        print("\nFirst 5 Artists")
        print("---------------")
        for artist in artist_repo.search("")[:5]:
            print(f"{artist.discogs_artist_id}: {artist.name}")

        print("\nFirst 5 Labels")
        print("--------------")
        for label in label_repo.search("")[:5]:
            print(f"{label.discogs_label_id}: {label.name}")

    finally:
        session.close()


if __name__ == "__main__":
    main()