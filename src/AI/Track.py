class Track:
    anyTrack = None

    def __init__(self, Connection):
        self.conn = Connection

    def FromNone(self):
        return Track(None)

