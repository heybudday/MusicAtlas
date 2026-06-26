from app.models.release import Release
from app.models.session import SessionLocal


def main():
    session = SessionLocal()

    try:
        release = session.query(Release).first()

        if release is None:
            print("No releases found.")
            return

        print(f"Release ID: {release.discogs_release_id}")
        print(f"Title: {release.title}")
        print(f"Year: {release.released_year}")

    finally:
        session.close()


if __name__ == "__main__":
    main()