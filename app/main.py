from pathlib import Path

from database import Base, engine


def initialize_database():
    """Create the SQLite database if it doesn't already exist."""
    Base.metadata.create_all(engine)


def main():
    print("=" * 40)
    print("Music Atlas")
    print("=" * 40)

    initialize_database()

    project_root = Path(__file__).resolve().parent.parent

    print(f"Project: {project_root}")
    print("Database initialized.")
    print("Ready.")


if __name__ == "__main__":
    main()