import sys

from src.Enums import Colors
from src.Players import Player


class Connection:
    def __init__(self, id, size, colors, cities, double=False):
        self.owner1 = None
        self.owner2 = None
        self.size = int(size)
        self.color = colors
        self.cities = cities
        self.id = int(id)
        self.double = double

    def getCost(self, player):
        if self.owner1 == player or self.owner2 == player:
            return 0
        if self.owner1 is not None and self.owner2 is not None:
            return 42
        if len(self.color) == 1 and self.owner1 is not None:
            return 42
        if len(self.color) == 2 and not self.double and (self.owner1 is not None or self.owner2 is not None):
            return 42

        return self.size

    def canClaim(self, player: Player) -> bool:
        if self.owner1 == player or self.owner2 == player:
            return False
        if self.owner1 is not None and self.owner2 is not None:
            return False
        if len(self.color) == 1 and self.owner1 is not None:
            return False
        if len(self.color) == 2 and not self.double and (self.owner1 is not None or self.owner2 is not None):
            return False

        return self.size <= player.Wagons

    def hasResources(self, cards):
        result = self.getResourcesType(cards)
        if len(result) > 0:
            return True
        return False

    def getResourcesType(self, cards):
        result = []
        if len(self.color) == 2:
            tmpSum = self.sumColors(self.color[1], cards)

            if tmpSum >= self.size and self.owner2 is None:
                result.append(self.color[1])

        sum1 = self.sumColors(self.color[0], cards)

        if sum1 >= self.size and self.owner1 is None:
            result.append(self.color[0])

        return result

    def sumColors(self, color, cards):
        if color == Colors.Colors.Rainbow:
            max = 0
            for i in Colors.Colors:
                if i == Colors.Colors.Rainbow:
                    continue
                tmp = cards[i] + cards[Colors.Colors.Rainbow]
                if tmp > max:
                    max = tmp
            return max
        else:
            return cards[color] + cards[Colors.Colors.Rainbow]

    def claim(self, player, cards, cardcolor):
        if not self.canClaim(player):
            return
        if not self.hasResources(cards):
            return

        if len(self.color) > 1:
            if cardcolor == self.color[0] and self.owner1 is None:
                self.owner1 = player
            elif cardcolor == self.color[1] and self.owner2 is None:
                self.owner2 = player
        else:
            self.owner1 = player
        player.Wagons -= self.size

    def countClaimed(self):
        pass

    def countToClaim(self):
        pass
