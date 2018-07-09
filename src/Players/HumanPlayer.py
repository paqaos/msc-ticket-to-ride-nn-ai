from src.Enums import Colors
from src.Enums.DecisionType import DecisionType
from src.Helpers.ShortestConnection import ShortestConnection
from src.Helpers.StatePrint import StatePrint
from src.Players.Player import Player
from src.Players.TicketDecision import TicketDecision
from src.Players.TrackDecision import TrackDecision
from src.Players.WagonDecision import WagonDecision


class HumanPlayer(Player):
    def __init__(self, name, game, board):
        Player.__init__(self, name, game, board)
        self.__targets__ = []

    def calculateDecision(self, game, board, state):
        print('choose your decision\n1. draw tickets\n2. draw wagons\n3. claim track')
        print('4. show status\n5. show wagons and tickets\n')
        active = True
        while active:
            line = input("choose")
            if line == '1':
                return DecisionType.TICKETCARD
            elif line == '2':
                return DecisionType.WAGONCARD
            elif line == '3':
                return DecisionType.CLAIMTRACK
            elif line == '4':
                for player in game.players:
                    print(player.PlayerName + ' (pt. ' + str(player.Points) + ') - ' + str(player.Wagons) + ' wagons')
                continue
            elif line == '5':
                colHow = {}
                for color in Colors.Colors:
                    colHow[color] = 0

                for card in self.WagonCards.cards:
                    colHow[card.Color] = colHow[card.Color] + 1

                for cardCount in colHow.items():
                    print(str(cardCount[0]) + ' ' + str(cardCount[1]))

                for ticket in self.TicketCards:
                    shpath = ShortestConnection.calculatePath(board, self, ticket.cities[1], ticket.cities[0])
                    for path in shpath:
                        print(path.cities[0].name + ' <-> ' + path.cities[1].name)
                    print(str(ticket.cities[0].name) \
                          + ' <-> ' + str(ticket.cities[1].name) + ' ( ' + str(ticket.points) + ' )' + str(ticket.Done))
            elif line == '6':
                StatePrint.printState(self.game, self, self.game.board)

    def drawTickets(self, min, tickets):
        choosed = []
        result = tickets
        active = True
        decision = TicketDecision()

        while active:
            print('choose ' + str(min) + ' tickets from collection: (provide id of ticket)\n')
            for ticket in result:
                print(str(ticket.id) + ': ' + str(ticket.cities[0].name)\
                      + ' <-> ' + str(ticket.cities[1].name) + ' ( ' + str(ticket.points) + ' )')

            if len(choosed) < min:
                line = input('please choose\n')
            else:
                line = input('please choose or "e" for end\n')
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

    def claimTrack(self, board):
        result = TrackDecision()
        available = []
        countCards = self.countCards()
        for connection in board.Connections:
            if connection.canClaim(self) and connection.hasResources(countCards):
                available.append(connection)
                print(str(connection.id) + ': ' + str(connection.cities[0].name) \
                      + ' <-> ' + str(connection.cities[1].name) + ' - size ' + str(connection.size))

        if len(available) > 0:
            left = 1
            while left > 0:
                select = input('select connection')
                selectInt = int(select)
                for conn in available:
                    if conn.id == selectInt:
                        result.conn = conn
                        left = 0

            leftCards = result.conn.size
            trackColors = result.conn.getResourcesType(countCards)

            toChose = []
            if trackColors[0] == Colors.Colors.Rainbow:
                rainbowCount = countCards[Colors.Colors.Rainbow]
                for color in countCards.keys():
                    if color == Colors.Colors.Rainbow and rainbowCount > leftCards:
                        toChose.append(Colors.Colors.Rainbow)
                    else:
                        sumCount =  countCards[color] + rainbowCount
                        if sumCount > leftCards:
                            toChose.append(color)
            else:
                rainbowCount = countCards[Colors.Colors.Rainbow]
                for tr in trackColors:
                    sumCount = countCards[tr] + rainbowCount
                    if sumCount > leftCards:
                        toChose.append(tr)

            id = 1
            for i in toChose:
                print('select #' + str(id) + ' to color' + str(i))
                id += 1

            selectedColor = None
            while selectedColor is None:
                color = int(input('select wagons to use'))
                if 0 < color < id:
                    selectedColor = toChose[color - 1]

            if trackColors[0] == Colors.Colors.Rainbow:
                result.color = Colors.Colors.Rainbow
            else:
                result.color = selectedColor

            if selectedColor == Colors.Colors.Rainbow:
                raincards = self.getCards(Colors.Colors.Rainbow, leftCards)
                for colorCard in raincards:
                    result.cards.append(colorCard)
            else:
                colorcards = self.getCards(selectedColor, leftCards)
                leftCards = leftCards - len(colorcards)
                raincards = self.getCards(Colors.Colors.Rainbow, leftCards)

                for colorCard in colorcards:
                    result.cards.append(colorCard)
                for colorCard in raincards:
                    result.cards.append(colorCard)

            return result
        else:
            print('cannot claim track')

    def drawWagons(self, wagonHand, isDeck, count):
        left = count
        decision = WagonDecision(None, None)
        while left > 0:
            print('chose wagons')
            for i in range(len(wagonHand.cards)):
                if left > 1:
                    print(str(i+1) + ' ' + str(wagonHand.cards[i].Color))
                else:
                    if wagonHand.cards[i].Color == Colors.Colors.Rainbow:
                        print('x' + str(Colors.Colors.Rainbow))
                    else:
                        print(str(i+1) + ' ' + str(wagonHand.cards[i].Color))

            if isDeck:
                print('d - draw from deck')

            line = input('please provide card id or d \n')
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
