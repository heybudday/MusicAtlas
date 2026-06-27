from __future__ import annotations


SEPARATOR = "-" * 50


class ReviewQueueCLI:
    def __init__(
        self,
        queue_service=None,
        decision_service=None,
        input_func=input,
        output_func=print,
    ):
        self.queue_service = queue_service
        self.decision_service = decision_service
        self.input_func = input_func
        self.output_func = output_func

    def run(self):
        items = self.queue_service.pending()

        if not items:
            self.output_func("No pending review items.")
            return 0

        for item in items:
            should_continue = self._process_item(item)
            if not should_continue:
                break

        return 0

    def _process_item(self, item):
        while True:
            self._display_item(item)
            choice = self.input_func("Choice: ").strip().lower()

            if choice in {"a", "approve"}:
                self.decision_service.approve(item)
                self.output_func("Approved.")
                return True

            if choice in {"r", "reject"}:
                self.decision_service.reject(item)
                self.output_func("Rejected.")
                return True

            if choice in {"s", "skip"}:
                self.output_func("Skipped.")
                return True

            if choice in {"q", "quit"}:
                self.output_func("Quitting review queue.")
                return False

            self.output_func("Invalid choice. Use A, R, S, or Q.")

    def _display_item(self, item):
        self.output_func(SEPARATOR)
        self.output_func(f"Artist: {self._value(item, 'artist_name')}")
        self.output_func("")
        self.output_func(f"Provider: {self._value(item, 'provider')}")
        self.output_func(f"Confidence: {self._value(item, 'confidence')}")
        self.output_func("")
        self.output_func("Recommended Match:")
        self.output_func(str(self._value(item, 'match_url') or ""))
        self.output_func("")
        self.output_func("[A]pprove")
        self.output_func("[R]eject")
        self.output_func("[S]kip")
        self.output_func("[Q]uit")
        self.output_func("")

    def _value(self, item, name):
        if isinstance(item, dict):
            return item.get(name)
        return getattr(item, name, None)


def main():
    from app.database import SessionLocal
    from app.services.review_decision_service import ReviewDecisionService
    from app.services.review_queue_service import ReviewQueueService

    session = SessionLocal()

    try:
        queue_service = ReviewQueueService(session)
        decision_service = ReviewDecisionService(session)

        cli = ReviewQueueCLI(
            queue_service=queue_service,
            decision_service=decision_service,
        )

        return cli.run()
    finally:
        session.close()


if __name__ == "__main__":
    raise SystemExit(main())