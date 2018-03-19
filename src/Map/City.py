class City:
    Connections = []
    Tickets = []

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def setConnection(self, conn):
        self.Connections.append(conn)
        conn.cities.append(self)

    def setDestination(self, ticket):
        self.Tickets.append(ticket)
        ticket.cities.append(self)
