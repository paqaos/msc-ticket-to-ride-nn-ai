import statistics

from src.Enums.Colors import Colors


class StatePrint:
    @staticmethod
    def printState(game, player):
        output = []
        output.append(int(player.Id))
        output.append(int(game.turn))

        wagonCards = player.countCards()

        for a in Colors:
            output.append(wagonCards[a])

        output.append(len(player.TicketCards))
        output.append(player.Wagons)
        output.append(player.Points)

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
            if player.Points > maxPoints:
                maxPoints = player.Points
            if player.Points < minPoints:
                minPoints = player.Points
            points.append(player.Points)
            sumPoints += player.Points

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

        medianPoints = statistics.median(points)
        avgPoints = sumPoints / len(points)
        medianWagons = statistics.median(wagons)
        avgWagons = sumWagons / len(wagons)
        medianTickets = statistics.median(tickets)
        avgTickets = sumTickets / len(tickets)
        medianWagonCards = statistics.median(wagonCards)
        avgWagonCards = sumWagonCards / len(wagonCards)

        output.append(minPoints)
        output.append(maxPoints)
        output.append(avgPoints)
        output.append(medianPoints)

        output.append(minWagon)
        output.append(maxWagon)
        output.append(avgWagons)
        output.append(medianWagons)

        output.append(minTickets)
        output.append(maxTickets)
        output.append(avgTickets)
        output.append(medianTickets)

        output.append(minWagonCards)
        output.append(maxWagonCards)
        output.append(avgWagonCards)
        output.append(medianWagonCards)

        return output

        # nr of tickets (uncompleted)
        # nr of all tickets
        # nr of wagons
        # points
        # missing to shortest path

        # points (min, max, average, median)
        # number of players
        # wagons (min, max, average, median)
