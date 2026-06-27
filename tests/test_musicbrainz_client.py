from unittest.mock import Mock, patch

from app.clients.musicbrainz import MusicBrainzClient


@patch("app.clients.musicbrainz.requests.get")
def test_search_artist(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "artists": [
            {
                "id": "1234-abcd",
                "name": "Jeff Mills",
                "score": "100",
            }
        ]
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    client = MusicBrainzClient()

    result = client.search_artist("Jeff Mills")

    assert result == {
        "id": "1234-abcd",
        "name": "Jeff Mills",
        "score": 100,
    }

    mock_get.assert_called_once()


@patch("app.clients.musicbrainz.requests.get")
def test_search_artist_not_found(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "artists": []
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    client = MusicBrainzClient()

    assert client.search_artist("Unknown Artist") is None


@patch("app.clients.musicbrainz.requests.get")
def test_search_label(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "labels": [
            {
                "id": "abcd-5678",
                "name": "Warp Records",
                "score": "100",
            }
        ]
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    client = MusicBrainzClient()

    result = client.search_label("Warp Records")

    assert result == {
        "id": "abcd-5678",
        "name": "Warp Records",
        "score": 100,
    }

    mock_get.assert_called_once()


@patch("app.clients.musicbrainz.requests.get")
def test_search_label_not_found(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "labels": []
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    client = MusicBrainzClient()

    assert client.search_label("Unknown Label") is None