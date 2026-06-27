from app.services.identity_orchestrator import IdentityOrchestrator


def test_artist_orchestrator_calls_provider():
    orchestrator = IdentityOrchestrator()

    try:
        orchestrator.enrich_artist("Jeff Mills", ["discogs"])
        assert False
    except NotImplementedError:
        pass


def test_label_orchestrator_calls_provider():
    orchestrator = IdentityOrchestrator()

    try:
        orchestrator.enrich_label("Warp Records", ["musicbrainz"])
        assert False
    except NotImplementedError:
        pass