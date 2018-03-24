from src.Collections.Hand import Hand
from src.Enums import DecisionType
from src.Enums.Colors import Colors
from src.Players.TicketDecision import TicketDecision
from src.Players.TrackDecision import TrackDecision
from src.Players.WagonDecision import WagonDecision


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
        return TrackDecision()

    def decisionTicket(self, board, game, cards, min):
        decision = TicketDecision()
        while len(decision.selected) < min:
            decision = self.drawTickets(min, cards)

        for sel in decision.selected:
            self.addTicket(sel)

        for rej in decision.rejected:
            self.rejectTicket(rej, board)

    def decisionWagons(self, board, game):
        account = 2
        while account > 0:
            decision = self.drawWagons(board.wagonsHand, board.wagonsDeck.canDraw(1), account)

            if decision.type == WagonDecision.Deck and board.wagonsDeck.canDraw(1):
                account = account - 1
                card = board.wagonsDeck.draw(1)[0]
                self.WagonCards.addCards([card])
            elif decision.type == WagonDecision.Rainbow and decision.card in board.wagonsHand.cards \
                    and Colors.Rainbow == decision.card.Color:
                account = account - 2
                card = board.wagonsHand.draw(decision.card)
                self.WagonCards.addCards([card])
            elif decision.card is not None:
                account = account - 1
                card = board.wagonsHand.draw(decision.card)
                self.WagonCards.addCards([card])

            board.refreshHand()
            board.refreshWagons()

    def decisionTrack(self, board, game):
        done = False
        while not done:
            trackDecision = self.claimTrack(board)
            cost = trackDecision.conn.getCost()
            if trackDecision.conn is not None and 0 < cost < 7 and self.canAfford(trackDecision):
                trackDecision.conn.claim(self, trackDecision.cards)
                for card in trackDecision.cards:
                    self.WagonCards.cards.remove(card)

                board.wagonGraveyard.addCards(trackDecision.cards)

    def canAfford(self, track):
        return False

    def drawTickets(self, min, tickets):
        return TicketDecision()

    def addTicket(self, card):
        self.TicketCards.append(card)

    def rejectTicket(self, card, board):
        board.ticketDeck.cards.append(card)

    def drawWagons(self, wagonHand, isDeck, count):
        return WagonDecision()

