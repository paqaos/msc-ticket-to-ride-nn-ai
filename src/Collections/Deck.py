class Deck:
    def __init__(self):
        self.cards = []

    def canDraw(self, count):
        return min(count, len(self.cards))

    def draw(self):
        if self.candraw(1) == 1:
            card = self.cards[0]
            self.cards.remove(card)
            return card
        else:
            return None

    def draw(self, count):
        amount = self.canDraw(count)
        result = []
        for i in range(amount):
            card = self.cards[0]
            self.cards.remove(card)
            result.append(card)

        return result

    def add(self, card):
        self.cards.append(card)

    def addCards(self, cards):
        for card in cards:
            self.cards.append(card)

