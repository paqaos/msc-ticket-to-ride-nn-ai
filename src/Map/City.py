class City:
    Connections = []

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def setConnection(self, conn):
        self.Connections.append(conn)
        conn.cities.append(self)
