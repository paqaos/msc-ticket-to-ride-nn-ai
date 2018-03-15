import random

from src.Cards.WagonCard import WagonCard
from src.Collections.Deck import Deck
from src.Enums import Colors

class Board:
    def __init__(self):
        self.wagonsDeck = Deck()
        self.ticketDeck = Deck()
        self.wagonGraveyard = Deck()
        self.__prepareCards__()

    def __prepareCards__(self):
        for color in Colors.Colors:
            for i in range(12):
                card = WagonCard(color)
                self.wagonsDeck.add(card)

        for i in range(2):
            self.wagonsDeck.add(WagonCard(Colors.Colors.Rainbow))

        random.shuffle(self.wagonsDeck.cards)
