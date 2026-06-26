from sqlalchemy import text

from app.database import SessionLocal


def main():
    session = SessionLocal()

    try:
        tables = ["releases", "artists", "labels"]

        print("Database Contents")
        print("=================\n")

        for table in tables:
            count = session.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            ).scalar_one()

            print(f"{table:<10} {count:,} rows")

    finally:
        session.close()


if __name__ == "__main__":
    main()