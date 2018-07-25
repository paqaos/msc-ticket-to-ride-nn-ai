import statistics

from src.Enums.Colors import Colors


class StatePrint:
    @staticmethod
    def printState(game, player):
        output = []
        output.append(int(game.turn))
        output.append(len(player.WagonCards.cards))
        output.append(len(game.board.wagonsHand.cards))
        output.append(len(game.board.wagonsDeck.cards))
        output.append(len(game.board.wagonGraveyard.cards))
        output.append(len(player.TicketCards))
        output.append(len(game.board.ticketDeck.cards))
        output.append(player.Wagons)
        output.append(player.Points)

        wagonCards = player.countCapacity()
        max = 0
        diff = 0
        for wagonCard in wagonCards:
            if wagonCards[wagonCard] > 0:
                diff += 1
            if wagonCards[wagonCard] > max:
                max = wagonCards[wagonCard]

        output.append(len(game.board.wagonsDeck.cards) +  len(game.board.wagonsHand.cards))

        output.append(len(player.__poss__))
        output.append(len(player.__match__))
        output.append(len(player.__targets__))
        output.append(len(player.__lack__))
        output.append(len(game.players))

        points = []
        wagons = []
        tickets = []
        wagonCards = []
        minWagon = float("inf")
        maxWagon = 0
        minPoints = float("inf")
        maxPoints = 0
        minTickets = float("inf")
        maxTickets = 0
        minWagonCards = float("inf")
        maxWagonCards = 0
        sumPoints = 0
        sumWagons = 0
        sumTickets = 0
        sumWagonCards = 0
        for player in game.players:
            if player.PointsForOthers > maxPoints:
                maxPoints = player.PointsForOthers
            if player.PointsForOthers < minPoints:
                minPoints = player.PointsForOthers
            points.append(player.PointsForOthers)
            sumPoints += player.PointsForOthers

            if player.Wagons > maxWagon:
                maxWagon = player.Wagons
            if player.Wagons < minWagon:
                minWagon = player.Wagons
            wagons.append(player.Wagons)
            sumWagons += player.Wagons

            ticketsCount = len(player.TicketCards)
            wagonCount = len(player.WagonCards.cards)

            if ticketsCount > maxTickets:
                maxTickets = ticketsCount
            if ticketsCount < minTickets:
                minTickets = ticketsCount
            tickets.append(ticketsCount)
            sumTickets += ticketsCount

            if wagonCount > maxWagonCards:
                maxWagonCards = wagonCount
            if wagonCount < minWagonCards:
                minWagonCards = wagonCount
            wagonCards.append(wagonCount)
            sumWagonCards += wagonCount

        medianWagons = statistics.median(wagons)
        avgWagons = sumWagons / len(wagons)
        medianTickets = statistics.median(tickets)
        avgTickets = sumTickets / len(tickets)

        output.append(minWagon)
        output.append(maxWagon)
        output.append(avgWagons)
        output.append(medianWagons)

        output.append(minTickets)
        output.append(maxTickets)
        output.append(avgTickets)
        output.append(medianTickets)

        output.append(player.TicketFail)
        output.append(player.TicketDone)
        output.append(player.PointsForOthers)

        output.append(max)
        output.append(diff)

        return output
