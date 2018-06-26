from src.Helpers.ShortestPath import ShortestPath


class TicketConnection:
    @staticmethod
    def CheckConnection(board, ticket, player):
        distance = ShortestPath.calculate(board, player, ticket.cities[0], ticket.cities[1])

        if distance == 0:
            ticket.Done = True
            return None
        elif distance is not None:
            return True
        else:
            return False