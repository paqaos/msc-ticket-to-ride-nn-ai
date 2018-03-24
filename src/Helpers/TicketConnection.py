from src.Helpers import ShortestPath


class TicketConnection:
    @staticmethod
    def CheckConnection(board, ticket, player):
        distance = ShortestPath.calculate(board, ticket.cities[0], ticket.cities[1], player)

        if distance == 0:
            ticket.Done = True
        elif distance is not None:
            return True
        else:
            return False