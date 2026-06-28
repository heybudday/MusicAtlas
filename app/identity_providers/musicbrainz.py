class MusicBrainzProvider:
    def __init__(self, client=None):
        self.client = client

    def lookup_artist(self, name):
        return {
            "matched": True,
            "name": name,
        }

    def lookup_label(self, name):
        return {
            "matched": True,
            "name": name,
        }