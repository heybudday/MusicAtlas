from app.models import Release
from app.models.session import SessionLocal


def main():
    with SessionLocal() as session:
        release = (
            session.query(Release)
            .filter_by(discogs_release_id=1)
            .first()
        )

        if release is None:
            print("Release not found.")
            return

        print("=" * 34)
        print("Release")
        print("=" * 34)
        print()
        print(f"Title: {release.title}")
        print(f"Year : {release.released_year}")
        print()

        print("Artists")
        print("-------")
        if hasattr(release, "release_artists"):
            for ra in release.release_artists:
                if getattr(ra, "artist", None):
                    print(ra.artist.name)
                else:
                    print(ra.artist_key)
        else:
            print("No release_artists relationship found.")

        print()

        print("Labels")
        print("------")
        if hasattr(release, "release_labels"):
            for rl in release.release_labels:
                if getattr(rl, "label", None):
                    print(rl.label.name)
                else:
                    print(rl.label_key)
        else:
            print("No release_labels relationship found.")

        print()

        print("Tracks")
        print("------")
        if hasattr(release, "tracks"):
            for track in release.tracks:
                print(f"{track.track_position} {track.title}")

                if hasattr(track, "artist_links"):
                    for ta in track.artist_links:
                        if getattr(ta, "artist", None):
                            print(f"    {ta.artist.name}")
                        else:
                            print(f"    {ta.artist_key}")
        else:
            print("No tracks relationship found.")


if __name__ == "__main__":
    main()