from app.identity_providers.registry import create_default_registry


def test_default_registry():
    registry = create_default_registry()

    names = registry.service_names()

    assert "discogs" in names
    assert "musicbrainz" in names
    assert "spotify" in names

    assert registry.get("discogs") is not None
    assert registry.get("musicbrainz") is not None
    assert registry.get("spotify") is not None

    assert registry.get("does_not_exist") is None