from app.repositories.identity_resolution_repository import (
    IdentityResolutionRepository,
)


def test_repository_returns_empty_list_without_session():
    repository = IdentityResolutionRepository()

    assert repository.all() == []


def test_repository_returns_empty_list_with_session_placeholder():
    class FakeSession:
        pass

    repository = IdentityResolutionRepository(FakeSession())

    assert repository.all() == []