from src.Enums import DecisionType


class Player:
    Active = True
    Last = False
    Wagons = 45
    TicketCards = []
    WagonCards = []

    def __init__(self, name):
        self.PlayerName = name
    def calculateDecision(self, board):
        return DecisionType.CLAIMTRACK

    def claimTrack(self, board):
        pass
