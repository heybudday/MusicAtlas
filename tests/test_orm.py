from app.models import Release
from app.models.session import SessionLocal


def main():
    with SessionLocal() as session:
        release = session.query(Release).first()

        if release is None:
            print("No releases found.")
            return

        print(f"Release ID: {release.discogs_release_id}")
        print(f"Title: {release.title}")
        print(f"Year: {release.released_year}")


if __name__ == "__main__":
    main()