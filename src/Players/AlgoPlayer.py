from random import random

from src.AI import Track
from src.Enums.DecisionType import DecisionType
from src.Helpers.ShortestConnection import ShortestConnection
from src.Players.Player import Player
import itertools

from src.Players.TicketDecision import TicketDecision


class AlgoPlayer(Player):
    def __init__(self, name, game, board):
        Player.__init__(self, name, game, board)
        self.__targets__ = []
        self.__lack__ = []
        self.__poss__ = []

    def canClaimTrack(self,track):
        return False

    def hasWagons(self, color):
        return False

    def hasAnyWagons(self, color):
        if color is not None:
            return self.countCards()[color]
        else:
            return len(self.WagonCards) > 0

    def calculateDecision(self, game, board):
        if len(self.TicketCards) > 0:
            turn = game.turn
            x = random() % (20+turn)
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

    def prepareTurn(self, board, game):
        self.__targets__.clear()

        target = []
        possible = []
        lack = []
        cards = self.countCards()

        for ticket in self.TicketCards:
            distance = ShortestConnection.calculatePath(self.board, self, ticket.cities[0], ticket.cities[1])
            target = list(set().union(target, distance))

        for c in board.Connections:
            if not c.hasResources(cards) or not c.canClaim(self):
                continue

            if len(target) > 0 and target.__contains__(c):
                possible.append(c)
            elif c.size > 5:
                possible.append(c)
            elif len(target) == 0:
                possible.append(c)

        for t in target:
            if not possible.__contains__(t):
                lack.append(t)
        self.__lack__ = lack
        self.__poss__ = possible
        self.__targets__ = target


    def drawTickets(self, min, tickets):
        result = []
        ticketSize = min
        ticketpoints = 0
        ticketcost = float("inf")

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

                if tgCost < ticketcost:
                    result = tg
                    ticketcost = tgCost
                    ticketpoints = tgPoints
                elif tgCost == ticketcost and tgPoints > ticketpoints:
                    result = tg
                    ticketcost = tgCost
                    ticketpoints = tgPoints

            ticketSize += 1

        for t in result:
            print('realizuje' + t.cities[0].name + ' ' + t.cities[1].name + ' po trasie')

            distance = ShortestConnection.calculatePath(self.board, self, t.cities[0], t.cities[1])
            for cn in distance:
                print (cn.cities[0].name + '->'+cn.cities[1].name)

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

    def drawWagons(self, wagonHand, deck, count):
        print(len(self.__poss__))
        return []
