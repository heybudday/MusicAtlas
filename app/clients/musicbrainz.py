import requests


BASE_URL = "https://musicbrainz.org/ws/2"


class MusicBrainzClient:
    """
    Client for interacting with the MusicBrainz web service.
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "MusicAtlas/0.1 (https://github.com/your-org/musicatlas)"
        }

    def search_artist(self, name):
        response = requests.get(
            f"{BASE_URL}/artist",
            params={
                "query": name,
                "fmt": "json",
                "limit": 1,
            },
            headers=self.headers,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        artists = data.get("artists", [])

        if not artists:
            return None

        artist = artists[0]

        return {
            "id": artist["id"],
            "name": artist["name"],
            "score": int(artist.get("score", 0)),
        }

    def search_label(self, name):
        raise NotImplementedError