from pathlib import Path


def main():
    print("=" * 40)
    print("Music Atlas")
    print("=" * 40)

    project_root = Path(__file__).resolve().parent.parent
    print(f"Project: {project_root}")

    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    print("Ready.")


if __name__ == "__main__":
    main()