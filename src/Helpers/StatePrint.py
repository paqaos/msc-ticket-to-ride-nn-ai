import sys

from src.Enums.Colors import Colors


class StatePrint:
    @staticmethod
    def printState(game, player, state):
        output = []
        output.append(int(player.Id))
        output.append(int(game.turn))

        wagonCards = player.countCards()

        for a in Colors:
            output.append(wagonCards[a])

        output.append(len(player.TicketCards))
        output.append(player.Wagons)
        output.append(player.Points)

        

        print(output)
        return output

        # nr of tickets (uncompleted)
        # nr of all tickets
        # nr of wagons
        # points
        # missing to shortest path

        # points (min, max, average, median)
        # number of players
        # wagons (min, max, average, median)
