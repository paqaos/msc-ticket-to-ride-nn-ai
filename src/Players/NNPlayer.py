from numpy.random import random

from src.Enums import DecisionType
from src.Players.Player import Player


class NNPlayer(Player):
    def __init__(self, name, game, board):
        Player.__init__(self, name, game, board)
        self.__targets__ = []

    def canClaimTrack(self,track):
        return False

    def hasWagons(self, color):
        return False

    def hasAnyWagons(self, color):
        return False

    def calculateDecision(self, game, board,state):
        if len(self.TicketCards) > 0:
            turn = board.turn
            x = random(20+turn)
            if len(self.WagonCards.cards) >= 8 and self.Wagons > 8:
                return DecisionType.TICKETCARD
            elif self.HasAnyWagons(5):
                return DecisionType.CLAIMTRACK
            elif x < 20:
                return DecisionType.WAGONCARD
            elif self.canClaimTrack(Track.FromNone()):
                return DecisionType.CLAIMTRACK
            else:
                return DecisionType.WAGONCARD
        else:
            if self.canClaimTrack(None):
                return DecisionType.CLAIMTRACK
            else:
                return DecisionType.WAGONCARD

    def drawTickets(self, min, tickets):
        result = []
        mapData = []
        for x in tickets:
            if min > 0:
                result.append(x)
            min = min - 1
        return result

    def drawWagons(self, wagonHand, deck, count):

        return []
