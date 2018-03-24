from src.Enums import Colors
from src.Enums.DecisionType import DecisionType
from src.Helpers.ShortestPath import ShortestPath
from src.Players.Player import Player
from src.Players.TicketDecision import TicketDecision
from src.Players.WagonDecision import WagonDecision


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
        choosed = []
        result = tickets
        active = True
        decision = TicketDecision()

        while active:
            print 'choose ' + str(min) + ' tickets from collection: (provide id of ticket)\n'
            for ticket in result:
                print str(ticket.id) + ': ' + str(ticket.cities[0].name)\
                      + ' <-> ' + str(ticket.cities[1].name) + ' ( ' + str(ticket.points) + ' )'

            if len(choosed) < min:
                line = raw_input('please choose\n')
            else:
                line = raw_input('please choose or "e" for end\n')
                if line == "e":
                    active = False

            for ticket in result:
                if ticket.id == line:
                    choosed.append(ticket)

            for chose in choosed:
                if chose in result:
                    result.remove(chose)

        for card in result:
            decision.rejected.append(card)

        for card in choosed:
            decision.selected.append(card)

        return decision

    def drawWagons(self, wagonHand, isDeck, count):
        left = count
        decision = WagonDecision(None, None)
        while left > 0:
            print 'chose wagons'
            for i in range(len(wagonHand.cards)):
                if left > 1:
                    print str(i+1) + ' ' + str(wagonHand.cards[i].Color)
                else:
                    if wagonHand.cards[i].Color == Colors.Colors.Rainbow:
                        print 'x' + str(Colors.Colors.Rainbow)
                    else:
                        print str(i+1) + ' ' + str(wagonHand.cards[i].Color)

            if isDeck:
                print 'd - draw from deck'

            line = raw_input('please provide card id or d \n')
            card = None
            if line == "1":
                card = wagonHand.cards[0]
            elif line == "2":
                card = wagonHand.cards[1]
            elif line == "3":
                card = wagonHand.cards[2]
            elif line == "4":
                card = wagonHand.cards[3]
            elif line == "5":
                card = wagonHand.cards[4]
            elif isDeck and line == "d":
                decision.type = decision.Deck
                return decision

            if card is not None:
                if card.Color == Colors.Colors.Rainbow:
                    decision.type = decision.Rainbow
                else:
                    decision.type = decision.Other

            decision.card = card
            return decision
