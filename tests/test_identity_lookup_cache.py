class FakeRepository:
    def __init__(self):
        self.saved = []

    def save(self, payload):
        self.saved.append(payload)

    def get(self, provider, entity_type, query):
        for item in self.saved:
            if (
                item.get("provider") == provider and
                item.get("entity_type") == entity_type and
                item.get("query") == query
            ):
                return item
        return None