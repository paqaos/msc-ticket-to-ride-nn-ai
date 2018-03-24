import sys


class Connection:
    def __init__(self, id, size, colors, cities):
        self.owner1 = None
        self.owner2 = None
        self.size = int(size)
        self.color = colors
        self.cities = cities
        self.id = id

    def getCost(self, player):
        if self.owner1 == player or self.owner2 == player:
            return 0
        if len(self.color) == 1 and (self.owner1 is not None or self.owner2 is not None):
            return sys.maxint
        if self.owner1 is not None or self.owner2 is not None:
            return sys.maxint

        return self.size
