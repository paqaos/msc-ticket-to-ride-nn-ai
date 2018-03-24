from src.Collections.Hand import Hand
from src.Enums import DecisionType
from src.Players.TicketDecision import TicketDecision


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
        decision = TicketDecision()
        while len(decision.selected) < min:
            decision = self.drawTickets(min, cards)

        for sel in decision.selected:
            self.addTicket(sel)

        for rej in decision.rejected:
            self.rejectTicket(rej, board)

    def drawTickets(self, min, tickets):
        return TicketDecision()

    def addTicket(self, card):
        self.TicketCards.append(card)

    def rejectTicket(self, card, board):
        board.ticketDeck.cards.append(card)

    def drawWagons(self, wagonHand, deck, count):
        pass

