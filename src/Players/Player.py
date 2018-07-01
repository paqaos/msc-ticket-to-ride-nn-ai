from src.Collections.Hand import Hand
from src.Enums import DecisionType
from src.Enums.Colors import Colors
from src.Helpers.DistancePointCalculator import DistancePointCalculator
from src.Helpers.TicketConnection import TicketConnection
from src.Players.TicketDecision import TicketDecision
from src.Players.TrackDecision import TrackDecision
from src.Players.WagonDecision import WagonDecision

class Player:

    def __init__(self, name, game, board):
        self.Id = game.playerId
        game.playerId += 1
        self.PlayerName = name
        self.Active = True
        self.Last = False
        self.Wagons = 45
        self.Points = 0
        self.TicketCards = []
        self.WagonCards = Hand()
        self.game = game
        self.board = board
        self.decisions = [DecisionType.DecisionType.START]
        self.claimed = []

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

    def prepareTurn(self, board, game):
        pass

    def decisionWagons(self, board, game):
        account = 2
        while account > 0:
            if account == 1 and len(board.wagonsHand.cards) == 0 and len(board.wagonsDeck.cards) == 0:
                break
            decision = self.drawWagons(board.wagonsHand, board.wagonsDeck, board.wagonsDeck.canDraw(1), account)

            if decision.type == WagonDecision.Deck and board.wagonsDeck.canDraw(1):
                account = account - 1
                card = board.wagonsDeck.draw(1)[0]
                self.WagonCards.addCards([card])
            elif decision.type == WagonDecision.Rainbow and Colors.Rainbow == decision.card.Color:
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
            cost = trackDecision.conn.getCost(self)
            if trackDecision.conn is not None and 0 < cost < 7 and self.canAfford(trackDecision):

                trackDecision.conn.claim(self, self.countHandCards(trackDecision.cards), trackDecision.color)
                for card in trackDecision.cards:
                    self.WagonCards.cards.remove(card)

                print('claimed ' + trackDecision.conn.cities[0].name + ' <-> ' + trackDecision.conn.cities[1].name + 'size' + str(trackDecision.conn.size))
                board.wagonGraveyard.addCards(trackDecision.cards)
                self.claimed.append(trackDecision.conn)
                done = True

    def canAfford(self, track):
        sizeCost = track.conn.size
        trackColor = track.color

        for a in track.cards:
            if a.Color == Colors.Rainbow:
                sizeCost -= 1
            elif a.Color == trackColor:
                sizeCost -= 1
            elif a.Color != trackColor and trackColor == Colors.Rainbow:
                sizeCost -= 1

        return sizeCost == 0

    def drawTickets(self, min, tickets):
        return TicketDecision()

    def addTicket(self, card):
        self.TicketCards.append(card)

    def rejectTicket(self, card, board):
        board.ticketDeck.cards.append(card)

    def drawWagons(self, wagonHand, deck, isDeck, count):
        return WagonDecision()

    def countCards(self):
        colHow = {}
        for color in Colors:
            colHow[color] = 0

        for card in self.WagonCards.cards:
            colHow[card.Color] = colHow[card.Color] + 1

        return colHow

    def countHandCards(self, altcards):
        colHow = {}
        for color in Colors:
            colHow[color] = 0

        for card in altcards:
            colHow[card.Color] = colHow[card.Color] + 1

        return colHow

    def countCapacity(self):
        capacity = {}
        for color in Colors:
            capacity[color] = 0

        for card in self.WagonCards.cards:
            capacity[card.Color] = capacity[card.Color] + 1

        maxCount = 0
        rainbow = capacity[Colors.Rainbow]
        for color in Colors:
            if color != Colors.Rainbow:
                if capacity[color] > maxCount:
                    maxCount = capacity[color]
                capacity[color] += rainbow

        capacity[Colors.Rainbow] += maxCount
        return capacity


    def getCards(self, cardColor, count):
        result = []
        for card in self.WagonCards.cards:
            if card.Color == cardColor and count > 0:
                result.append(card)
                count -= 1
        for card in result:
            self.WagonCards.draw(card)
        return result

    def HasAnyWagons(self, number):
        cards = self.countCards()

        check = False
        for card in cards:
            if cards[card] >= number:
                check = True
        return check

    def calculatePoints(self, board):
        points = 0
        ticketPoints = 0
        trackPoints = 0
        tracks = { }
        for i in range(1,7):
            tracks[i] = 0
        for c in self.claimed:
            tracks[c.size] += 1

        for i in range(1, 7):
            mult = DistancePointCalculator.calculatePoints(i)
            trackPoints += (mult * tracks[i])
            points += (mult * tracks[i])
            print(self.PlayerName + '- tras o dlugosci ' + str(i) + ': ' + str(tracks[i]))
            print('punkty ' + str(tracks[i]) + ' * ' + str(mult) + ' = ' + str(mult * tracks[i]))

        for t in self.TicketCards:
            connectionCheck = TicketConnection.CheckConnection(board, t, self)
            if not t.Done:
                ticketPoints -= int(t.points)
                points -= int(t.points)
                print(self.PlayerName + ': nie zrealizowany bilet ' + str(t.points))
            else:
                ticketPoints += int(t.points)
                points += int(t.points)
                print(self.PlayerName + ': zrealizowany bilet ' + str(t.points))

        return (points, trackPoints, ticketPoints)

