import requests


BASE_URL = "https://musicbrainz.org/ws/2"


class MusicBrainzClient:
    """
    Client for interacting with the MusicBrainz web service.
    """

    def search_artist(self, name):
        raise NotImplementedError

    def search_label(self, name):
        raise NotImplementedError