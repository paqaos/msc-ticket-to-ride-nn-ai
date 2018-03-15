from src.Collections.Deck import Deck


class Board:
    def __init__(self):
        self.wagonsDeck = Deck()
        self.ticketDeck = Deck()
        self.wagonGraveyard = Deck()
        pass
