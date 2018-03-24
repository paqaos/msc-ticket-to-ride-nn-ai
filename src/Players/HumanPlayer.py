from src.Enums import Colors
from src.Enums.DecisionType import DecisionType
from src.Helpers.ShortestPath import ShortestPath
from src.Players.Player import Player


class HumanPlayer(Player):
    def __init__(self, name, game, board):
        Player.__init__(self, name, game, board)
        self.__targets__ = []

    def calculateDecision(self, game, board):
        print 'choose your decision\n1. draw tickets\n2. draw wagons\n3. claim track'
        print '4. show status\n5. show wagons and tickets\n'
        active = True
        while active:
            line = raw_input("choose")
            if line == '1':
                return DecisionType.TICKETCARD
            elif line == '2':
                return DecisionType.WAGONCARD
            elif line == '4':
                for player in game.players:
                    print player.PlayerName + ' (pt. ' + str(player.Points) + ') - ' + str(player.Wagons) + ' wagons'
                continue
            elif line == '5':
                colHow = {}
                for color in Colors.Colors:
                    colHow[color] = 0

                for card in self.WagonCards.cards:
                    colHow[card.Color] = colHow[card.Color] + 1

                for cardCount in colHow.items():
                    print str(cardCount[0]) + ' ' + str(cardCount[1])

                for ticket in self.TicketCards:
                    ShortestPath.calculate(board, self, ticket.cities[1], ticket.cities[0])
                    print str(ticket.cities[0].name) \
                          + ' <-> ' + str(ticket.cities[1].name) + ' ( ' + str(ticket.points) + ' )' + str(ticket.Done)


    def drawTickets(self, min, tickets):
        chosed = []
        result = tickets
        active = True

        while active:
            print 'choose ' + str(min) + ' tickets from collection: (provide id of ticket)\n'
            for ticket in result:
                print str(ticket.id) + ': ' + str(ticket.cities[0].name)\
                      + ' <-> ' + str(ticket.cities[1].name) + ' ( ' + str(ticket.points) + ' )'

            if len(chosed) < min:
                line = raw_input('please choose\n')
            else:
                line = raw_input('please choose or "e" for end\n')
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

    def drawWagons(self, wagonHand, deck, count):
        left = count
        while left > 0:
            print 'chose wagons'
            for i in range(len(wagonHand.cards)):
                print str(i) + ' ' + str(wagonHand.cards[i].Color)

            if len(deck.cards) > 0:
                print 'd - draw from deck'

            line = raw_input('please provide card id or d \n')
            if line == "1":
                card = wagonHand.cards[0]
            elif line == "2":
                card == wagonHand.cards[1]
            elif line == "d":
                card = deck.draw(1)

            self.game.drawWagon(self, card)
            self.WagonCards.addCards({card})
            left = left - 1
