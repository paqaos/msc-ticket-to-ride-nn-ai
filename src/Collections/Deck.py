class Deck:
    def __init__(self):
        self.cards = []

    def canDraw(self):
        return len(self.cards) > 0

    def draw(self):
        if self.candraw():
            card = self.cards[0]
            self.cards.remove(card)
            return card
        else:
            return None

    def draw(self, count):
        pass

    def add(self, card):
        self.cards.append(card)

