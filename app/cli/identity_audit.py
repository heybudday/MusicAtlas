from __future__ import annotations

from app.database import SessionLocal
from app.services.identity_audit_runner import IdentityAuditRunner


def main():
    print("=" * 41)
    print("Music Atlas Identity Audit")
    print("=" * 41)
    print()

    session = SessionLocal()

    try:
        runner = IdentityAuditRunner(session)
        summary = runner.run_all()

        print(f"Processed:   {summary['processed']}")
        print(f"Successful: {summary['success']}")
        print(f"Review:     {summary['review']}")
        print(f"Failed:     {summary['failed']}")
        print()
        print("Done.")

    finally:
        session.close()


if __name__ == "__main__":
    main()