from random import random

from src.AI import Track
from src.Enums.Colors import Colors
from src.Enums.DecisionType import DecisionType
from src.Helpers.DistancePointCalculator import DistancePointCalculator
from src.Helpers.ShortestConnection import ShortestConnection
from src.Helpers.TicketConnection import TicketConnection
from src.Players.Player import Player
import itertools

from src.Players.TicketDecision import TicketDecision
from src.Players.TrackDecision import TrackDecision
from src.Players.WagonDecision import WagonDecision


class AlgoPlayer(Player):
    def __init__(self, name, game, board):
        Player.__init__(self, name, game, board)
        self.__targets__ = []
        self.__lack__ = []
        self.__poss__ = []
        self.__match__ = []

    def canClaimTrack(self, track):
        print(str(len(self.__match__)) + ' - ' + str(len(self.__targets__)) + ' - ' + str(len(self.__poss__)))
        return len(self.__match__) > 0 or (len(self.__targets__) == 0 and len(self.__poss__) > 0)

    def hasWagons(self, color):
        return False

    def hasAnyWagons(self, color):
        if color is not None:
            return self.countCards()[color]
        else:
            return len(self.WagonCards) > 0

    def calculateDecision(self, game, board):
        self.prepareTurn(board,game)
        activeTicket = False
        for tc in self.TicketCards:
            connectionCheck = TicketConnection.CheckConnection(board, tc, self)
            if not tc.Done:
                activeTicket = True

        canDrawWagons = len(board.wagonsDeck.cards) > 0 or len(board.wagonsHand.cards) > 0
        canClaim = len(self.__poss__) > 0
        if not activeTicket:
            turn = game.turn
            x = random() % (20 + turn)
            if len(self.WagonCards.cards) >= 8 and self.Wagons >= 8:
                return DecisionType.TICKETCARD
            elif self.HasAnyWagons(6) and canClaim:
                return DecisionType.CLAIMTRACK
            elif x < 20 and canDrawWagons:
                return DecisionType.WAGONCARD
            elif canClaim:
                return DecisionType.CLAIMTRACK
            elif canDrawWagons:
                return DecisionType.WAGONCARD
        else:
            if canClaim and self.canClaimTrack(None):
                return DecisionType.CLAIMTRACK
            elif canDrawWagons:
                return DecisionType.WAGONCARD

        return DecisionType.TICKETCARD # ostateczność

    def prepareTurn(self, board, game):
        target = []
        possible = []
        lack = []
        match = []
        cards = self.countCards()

        for ticket in self.TicketCards:
            distance = ShortestConnection.calculatePath(self.board, self, ticket.cities[0], ticket.cities[1])
            target = list(set().union(target, distance))

        for c in board.Connections:
            if not c.hasResources(cards) or not c.canClaim(self):
                continue

            if len(target) > 0 and target.__contains__(c):
                possible.append(c)
            elif c.size >= 6:
                possible.append(c)
                match.append(c)
            elif len(target) == 0:
                possible.append(c)

        finalTarget = []
        for t in target:
            if not c.canClaim(self):
                continue
            else:
                finalTarget.append(t)
                if not possible.__contains__(t):
                    lack.append(t)
                else:
                    match.append(t)

        self.__lack__ = lack
        self.__poss__ = possible
        self.__targets__ = finalTarget
        self.__match__ = match

    def drawTickets(self, min, tickets):
        result = None
        ticketSize = min
        ticketpoints = 0
        ticketcost = float("inf")
        reachable = False

        minPassing = None
        minCost = 100

        while ticketSize <= len(tickets):
            ticketGroups = itertools.combinations(tickets, ticketSize)

            for tg in ticketGroups:
                tgCost = 0
                tgPoints = 0

                connections = []
                for t in tg:
                    distance = ShortestConnection.calculatePath(self.board, self, t.cities[0], t.cities[1])
                    connections = list(set().union(connections, distance))
                    tgPoints += int(t.points)

                for con in connections:
                    if con.getCost(self) != 0:
                        tgCost += con.getCost(self)

                if tgCost >= self.Wagons:
                    if tgCost < minCost and (minPassing is None or len(minPassing) >= len(tg)):
                        minCost = tgCost
                        minPassing = tg
                    continue

                if tgCost < ticketcost:
                    result = tg
                    ticketcost = tgCost
                    ticketpoints = tgPoints
                elif tgCost == ticketcost and tgPoints > ticketpoints:
                    result = tg
                    ticketcost = tgCost
                    ticketpoints = tgPoints

            ticketSize += 1

        if result is None:
            result = minPassing

        for t in result:
            print( self.PlayerName +
                   'realizuje' + t.cities[0].name + ' ' + t.cities[1].name + ' po trasie')

            distance = ShortestConnection.calculatePath(self.board, self, t.cities[0], t.cities[1])
            for cn in distance:
                print(cn.cities[0].name + '->' + cn.cities[1].name)

        decision = TicketDecision()
        for x in result:
            decision.selected.append(x)
        for x in tickets:
            placed = False
            for x2 in result:
                if x2 == x:
                    placed = True
            if not placed:
                decision.rejected.append(x)
        return decision

    def drawWagons(self, wagonHand, deck, isdeck, count):
        trackColors = {}
        finalRequest = {}
        sumLacking = 0
        handColor = {}
        decision = WagonDecision(None, None)
        for color in Colors:
            trackColors[color] = 0
            handColor[color] = 0

        for hand in wagonHand.cards:
            handColor[hand.Color] += 1

        for a in self.__lack__:
            sumLacking += a.size
            for col in a.color:
                trackColors[col] = trackColors[col] + a.size

        maxWanted = 0
        mostWanted = None
        for b in trackColors:
            if trackColors[b] > 0:
                finalRequest[b] = trackColors[b]
                if maxWanted < finalRequest[b]:
                    maxWanted = finalRequest[b]
                    mostWanted = b

        if sumLacking == 0 and len(deck.cards) > 0:
            decision.type = WagonDecision.Deck
            return decision
        elif mostWanted is None and len(deck.cards) > 0:
            decision.type = WagonDecision.Deck
            return decision
        elif mostWanted is None and len(wagonHand.cards) > 0:
            cardFromHand = int(random() % len(wagonHand.cards))
            decision.type = WagonDecision.Other
            card = wagonHand.cards[cardFromHand]
            if card.Color == Colors.Rainbow:
                card = wagonHand.cards[0]
                decision.type = WagonDecision.Rainbow
            decision.card = card
            return decision
        if len(finalRequest) > 3 and len(deck.cards) >= 1:
            decision.type = WagonDecision.Deck
            return decision

        elif mostWanted is not None and sumLacking < 4 and handColor[mostWanted] > 0:
            decision.type = WagonDecision.Other

            for a in wagonHand:
                if a.color == mostWanted:
                    decision.card = a
                    break

            return decision
        elif sumLacking == 1 and wagonHand[Colors.Rainbow] > 0 and count > 1:
            decision.type = WagonDecision.Rainbow

            for a in wagonHand:
                if a.color == Colors.Rainbow:
                    decision.card = a
                    break

            return decision
        elif len(deck.cards) > 0:
            decision.type = WagonDecision.Deck
            return decision
        elif len(wagonHand.cards) > 0:
            cardFromHand = int(random() % len(wagonHand.cards))
            decision.type = WagonDecision.Other
            card = wagonHand.cards[cardFromHand]
            if card.Color == Colors.Rainbow:
                card = wagonHand.cards[0]
                decision.type = WagonDecision.Rainbow
            decision.card = card
            return decision

    def claimTrack(self, board):
        decision = TrackDecision()

        cardsCapacity = self.countCapacity()
        cards = self.countCards()

        trackColors = {}
        for color in Colors:
            trackColors[color] = 0

        for a in self.__lack__:
            for col in a.color:
                trackColors[col] = trackColors[col] + a.size

        mode = 0
        if len(self.__match__) > 0:
            mode = 1
            proccessing = self.__match__
        else:
            mode = 2
            proccessing = self.__poss__

        maxConn = None
        maxPoints = 0
        minCost = 7

        for con in proccessing:
            points = DistancePointCalculator.calculatePoints(con.size)
            if mode == 2 and points > maxPoints:
                maxConn = con
                maxPoints = points
            elif mode == 1 and con.size < minCost:
                minCost = con.size
                maxConn = con

        if maxConn is None:
            for con in self.__poss__:
                points = DistancePointCalculator.calculatePoints(con.size)
                if mode == 2 and points > maxPoints:
                    maxConn = con
                    maxPoints = points

        tmpColors = []
        if len(maxConn.color) == 1:
            tmpColors.append(maxConn.color[0])
        else:
            if maxConn.owner1 is None and cardsCapacity[maxConn.color[0]] >= maxConn.size:
                tmpColors.append(maxConn.color[0])
            if maxConn.owner2 is None and cardsCapacity[maxConn.color[1]] >= maxConn.size:
                tmpColors.append(maxConn.color[1])

        decision.conn = maxConn

        if len(tmpColors) == 1:
            decision.color = tmpColors[0]
        elif len(tmpColors) > 1:
            col1dif = trackColors[tmpColors[0]]
            col2dif = trackColors[tmpColors[1]]

            if col1dif > col2dif:
                decision.color = tmpColors[0]
            else:
                decision.color = tmpColors[1]

        col = decision.color

        if col == Colors.Rainbow:
            maxSingle = 0
            maxColor = None
            for a in Colors:
                if a is not Colors.Rainbow:
                    if maxSingle < cards[a]:
                        maxColor = a
                        maxSingle = cards[a]

            if maxSingle > decision.conn.size:
                maxSingle = decision.conn.size

            rainCols = decision.conn.size - maxSingle
            for a in self.WagonCards.cards:
                if maxColor is not None:
                    if a.Color == maxColor and maxSingle > 0:
                        decision.cards.append(a)
                        maxSingle -= 1
                if a.Color == Colors.Rainbow and rainCols > 0:
                    decision.cards.append(a)
                    rainCols -= 1

        else:
            colCal = cards[col]

            if colCal > decision.conn.size:
                colCal = decision.conn.size

            rainCol = decision.conn.size - colCal

            for a in self.WagonCards.cards:
                if a.Color == col and colCal > 0:
                    decision.cards.append(a)
                    colCal -= 1
                if a.Color == Colors.Rainbow and rainCol > 0:
                    decision.cards.append(a)
                    rainCol -= 1

        lenc = len(decision.cards) == decision.conn.size
        return decision
