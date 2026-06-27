import pytest


class FakeBind:
    def _run_ddl_visitor(self, *args, **kwargs):
        return None


class FakeQuery:
    def __init__(self, data):
        self._data = data
        self._filters = {}

    def filter_by(self, **kwargs):
        self._filters.update(kwargs)
        return self

    def _matches(self, item):
        for key, value in self._filters.items():
            if getattr(item, key, None) != value:
                return False

        return True

    def first(self):
        for item in self._data:
            if self._matches(item):
                return item

        return None

    def one(self):
        matches = [item for item in self._data if self._matches(item)]

        if len(matches) != 1:
            raise AssertionError(f"Expected exactly one result, got {len(matches)}")

        return matches[0]

    def all(self):
        return [item for item in self._data if self._matches(item)]


class FakeSession:
    def __init__(self):
        self.data = []

    def add(self, item):
        self.data.append(item)

    def commit(self):
        pass

    def get(self, *args, **kwargs):
        return None

    def execute(self, *args, **kwargs):
        return None

    def query(self, model):
        return FakeQuery(self.data)

    def get_bind(self):
        return FakeBind()


@pytest.fixture
def db_session():
    return FakeSession()