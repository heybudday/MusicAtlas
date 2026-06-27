from app.database import SessionLocal
from app.repositories.artist_repository import ArtistRepository
from app.repositories.label_repository import LabelRepository
from app.repositories.release_repository import ReleaseRepository
from app.repositories.track_repository import TrackRepository


def main():
    with SessionLocal() as session:
        release_repo = ReleaseRepository(session)
        artist_repo = ArtistRepository(session)
        label_repo = LabelRepository(session)
        track_repo = TrackRepository(session)

        release = release_repo.get_release_graph(1)

        print("==================================")
        print("Release Repository")
        print("==================================")

        if release is None:
            print("Release not found.")
            return

        print(f"Title: {release.title}")
        print(f"Year : {release.released_year}")

        print()
        print("Release Artists")
        print("---------------")
        for release_artist in release.release_artists:
            print(release_artist.artist_key)

        print()
        print("Release Labels")
        print("--------------")
        for release_label in release.release_labels:
            print(release_label.label_key)

        print()
        print("Tracks")
        print("------")
        tracks = track_repo.get_tracks_for_release(1)
        for track in tracks:
            print(f"{track.track_position}. {track.title}")

        print()
        print("Artist Lookup")
        print("-------------")
        artist = artist_repo.find_by_normalized_name("jeff mills")
        print(artist.name if artist else "Artist not found.")

        print()
        print("Label Lookup")
        print("------------")
        label = label_repo.find_by_normalized_name("warp records")
        print(label.name if label else "Label not found.")


if __name__ == "__main__":
    main()