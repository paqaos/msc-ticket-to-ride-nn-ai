from src.Player import Player


class AlgoPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def calculateDecision(self, board):
        if len(self.WagonCards.cards) > 0:
            pass
        else:
            pass

