class City:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.Connections = []
        self.Tickets = []

    def setConnection(self, conn):
        self.Connections.append(conn)
        conn.cities.append(self)

    def setDestination(self, ticket):
        self.Tickets.append(ticket)
        ticket.cities.append(self)
