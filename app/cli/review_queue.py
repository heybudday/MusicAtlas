from __future__ import annotations

import argparse
import json


def get_review_queue_class():
    try:
        from app.services.human_review_queue import HumanReviewQueue

        return HumanReviewQueue
    except ModuleNotFoundError:
        pass

    try:
        from app.services.identity_review_queue import HumanReviewQueue

        return HumanReviewQueue
    except ModuleNotFoundError:
        pass

    try:
        from app.services.review_queue import HumanReviewQueue

        return HumanReviewQueue
    except ModuleNotFoundError:
        pass

    return None


HumanReviewQueue = get_review_queue_class()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Music Atlas Human Review Queue"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output pending reviews as JSON",
    )
    return parser


def format_table(items):
    lines = [
        "========================================",
        "Music Atlas Review Queue",
        "========================================",
        "",
        f"Pending Reviews: {len(items)}",
        "",
    ]

    if not items:
        lines.append("No artists currently require manual review.")
        return "\n".join(lines)

    header = (
        f"{'ID':<6}"
        f"{'Artist':<30}"
        f"{'Confidence':<12}"
        f"Providers"
    )

    lines.append(header)
    lines.append("-" * len(header))

    for item in items:
        providers = ",".join(item.get("providers", []))

        lines.append(
            f"{item.get('artist_id', ''):<6}"
            f"{item.get('artist_name', ''):<30}"
            f"{item.get('confidence', 0):<12.2f}"
            f"{providers}"
        )

    return "\n".join(lines)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if HumanReviewQueue is None:
        items = []
    else:
        queue = HumanReviewQueue()
        items = queue.pending()

    if args.json:
        print(json.dumps(items, indent=2))
    else:
        print(format_table(items))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())