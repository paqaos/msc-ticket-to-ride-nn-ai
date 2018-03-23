import sys

from src.Enums.DecisionType import DecisionType
from src.Player import Player


class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.__targets__ = []

    def calculateDecision(self, board):
        print 'choose your decision\n1. draw tickets\n2. draw wagons\n3. claim track'
        for line in sys.stdin:
            if line == '1':
                return DecisionType.TICKETCARD
            elif line == '2':
                return DecisionType.WAGONCARD

    def drawTickets(self, min, tickets):
        chosed = []
        result = tickets
        active = True

        while active:
            print 'choose ' + str(min) + ' tickets from collection: (provide id of ticket)'
            for ticket in result:
                print str(ticket.id) + ': ' + str(ticket.cities[0].name)\
                      + ' <-> ' + str(ticket.cities[1].name) + ' ( ' + str(ticket.points) + ' )'

            if len(chosed) < min:
                line = raw_input('please chose')
            else:
                line = raw_input('please choose')
                if line == "e":
                    active = False

            for ticket in result:
                if ticket.id == line:
                    chosed.append(ticket)
                    self.TicketCards.append(ticket)

            for chose in chosed:
                if chose in result:
                    result.remove(chose)

        print 'thank you'
        return result
