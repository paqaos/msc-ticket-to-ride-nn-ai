from src.Collections.Hand import Hand
from src.Enums import DecisionType


class Player:
    def __init__(self, name):
        self.PlayerName = name
        self.Active = True
        self.Last = False
        self.Wagons = 45
        self.Points = 0
        self.TicketCards = []
        self.WagonCards = Hand()

    def calculateDecision(self, board):
        return DecisionType.CLAIMTRACK

    def claimTrack(self, board):
        pass

    def drawTickets(self, min, tickets):
        pass

    def drawWagons(self, wagonHand, deck, count):
        pass

