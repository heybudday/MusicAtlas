from app.database import SessionLocal
from app.services.identity_resolver import IdentityResolver


def main():
    session = SessionLocal()

    resolver = IdentityResolver(session)

    print("=" * 40)
    print("Artist Lookup")
    print("=" * 40)

    result = resolver.find_matching_artist("Jeff Mills")
    print(result)

    print()

    result = resolver.find_matching_artist("The Persuader")
    print(result)

    print()

    result = resolver.find_matching_artist("This Artist Does Not Exist")
    print(result)

    print()
    print("=" * 40)
    print("Label Lookup")
    print("=" * 40)

    result = resolver.find_matching_label("Svek")
    print(result)

    print()

    result = resolver.find_matching_label("Warp Records")
    print(result)

    print()

    result = resolver.find_matching_label("This Label Does Not Exist")
    print(result)

    session.close()


if __name__ == "__main__":
    main()