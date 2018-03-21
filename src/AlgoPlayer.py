from src.Player import Player


class AlgoPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def calculateDecision(self, board):
        if len(self.WagonCards.cards) > 0:
            pass
        else:
            pass

    def drawTickets(self, min, tickets):
        result = []
        for x in tickets:
            if min > 0:
                result.append(x)
            min = min - 1
        return result

