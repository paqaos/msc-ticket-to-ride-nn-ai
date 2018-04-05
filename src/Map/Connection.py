import sys

from src.Enums import Colors


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
        if (len(self.color) == 1 or not self.double) and (self.owner1 is not None or self.owner2 is not None):
            return sys.maxint
        if self.owner1 is not None or self.owner2 is not None:
            return sys.maxint

        return self.size

    def canClaim(self, player):
        if self.owner1 == player or self.owner2 == player:
            return False
        if (len(self.color) == 1 or not self.double) and (self.owner1 is not None or self.owner2 is not None):
            return False
        if self.owner1 is not None or self.owner2 is not None:
            return False

        return True

    def hasResources(self, cards):
        result = self.getResourcesType(cards)

        if len(result) > 0:
            return True
        else:
            return False

    def getResourcesType(self, cards):
        result = []
        if len(self.color) == 2:
            tmpSum = self.sumColors(self.color[1], cards)

            if tmpSum > self.size and self.owner2 is None:
                result.append(self.color[1])

        sum1 = self.sumColors(self.color[0], cards)

        if sum1 > self.size and self.owner1 is None:
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

    def claim(self, board, cards):
        pass

    def countClaimed(self):
        pass

    def countToClaim(self):
        pass
