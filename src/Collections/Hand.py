class Hand:
    def __init__(self):
        self.cards = []

    def canDraw(self):
        return len(self.cards) > 0

    def addCards(self, newCards):
        for card in newCards:
            self.cards.append(card)
