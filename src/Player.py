from src.Enums import DecisionType


class Player:
    def __init__(self, name):
        self.name = name

    def calculateDecision(self, board):
        return DecisionType.CLAIMTRACK