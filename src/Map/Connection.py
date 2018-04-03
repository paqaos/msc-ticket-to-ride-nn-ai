import sys


class Connection:
    def __init__(self, id, size, colors, cities, double=False):
        self.owner1 = None
        self.owner2 = None
        self.size = int(size)
        self.color = colors
        self.cities = cities
        self.id = id
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

    def claim(self, board, cards):
        pass
