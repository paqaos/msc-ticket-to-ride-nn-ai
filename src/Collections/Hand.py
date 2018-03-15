class Hand:
    def __init__(self):
        self.cards = []

    def canDraw(self):
        return len(self.cards) > 0