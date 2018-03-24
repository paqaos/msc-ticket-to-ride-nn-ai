from src.Collections.Hand import Hand
from src.Enums import DecisionType


class Player:
    def __init__(self, name, game, board):
        self.PlayerName = name
        self.Active = True
        self.Last = False
        self.Wagons = 45
        self.Points = 0
        self.TicketCards = []
        self.WagonCards = Hand()
        self.game = game
        self.board = board

    def calculateDecision(self, game, board):
        return DecisionType.CLAIMTRACK

    def claimTrack(self, board):
        pass

    def decisionTicket(self, board, game, cards, min):


    def drawTickets(self, min, tickets):
        pass

    def drawWagons(self, wagonHand, deck, count):
        pass

