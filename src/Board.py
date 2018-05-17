import random
import csv

from src.Cards.WagonCard import WagonCard
from src.Collections.Deck import Deck
from src.Collections.Hand import Hand
from src.Enums import Colors
from src.Map.City import City
from src.Map.Connection import Connection
from src.Map.Ticket import Ticket


class Board:
    def __init__(self):
        self.Cities = []
        self.Connections = []
        self.wagonsDeck = Deck()
        self.ticketDeck = Deck()
        self.wagonGraveyard = Deck()
        self.wagonsHand = Hand()
        self.__prepareMap__()
        self.__prepareCards__()

    def refreshWagons(self):
        if len(self.wagonsDeck.cards) == 0 and len(self.wagonGraveyard.cards) > 0:
            gravCards = self.wagonGraveyard.cards
            self.wagonGraveyard.cards = []
            random.shuffle(gravCards)
            self.wagonsDeck.addCards(gravCards)

    def checkHand(self):
        rainbows = 0
        for card in self.wagonsHand.cards:
            if card.Color == Colors.Colors.Rainbow:
                rainbows = rainbows + 1

        if rainbows > 2:
            self.wagonGraveyard.addCards(self.wagonsHand.cards)
            self.wagonsHand.cards = []
            self.refreshHand()

    def refreshHand(self):
        while len(self.wagonsDeck.cards) > 0 and len(self.wagonsHand.cards) < 5:
            self.refreshWagons()
            card = self.wagonsDeck.draw(1)[0]
            self.wagonsHand.addCards([card])
            self.checkHand()

    def __prepareCards__(self):
        for color in Colors.Colors:
            for i in range(12):
                card = WagonCard(color)
                self.wagonsDeck.add(card)

        for i in range(2):
            self.wagonsDeck.add(WagonCard(Colors.Colors.Rainbow))

        random.shuffle(self.wagonsDeck.cards)
        random.shuffle(self.ticketDeck.cards)

    def __prepareMap__(self):

        with open("data/usa/cities.csv", 'rt') as f:
            reader = csv.reader(f, delimiter=';')

            for line in reader:
                self.Cities.append(City(line[0], line[1]))

        with open("data/usa/connections.csv", 'rt') as f:
            reader = csv.reader(f, delimiter=';')

            for line in reader:
                conn = Connection(line[0], line[3], [], [])
                for x in self.Cities:
                    if x.id == line[1]:
                        city1 = x
                    if x.id == line[2]:
                        city2 = x

                if line[4] is not None and line[4] != '':
                    tmpColor = Colors.Colors.fromString(line[4])
                    if tmpColor is not None:
                        conn.color.append(tmpColor)
                if line[5] is not None and line[5] != '':
                    tmpColor = Colors.Colors.fromString(line[5])
                    if tmpColor is not None:
                        conn.color.append(tmpColor)
                city1.setConnection(conn)
                city2.setConnection(conn)
                self.Connections.append(conn)

        with open("data/usa/tickets.csv", "rt") as f:
            reader = csv.reader(f, delimiter=';')

            for line in reader:
                conn = Ticket(line[0], line[3], [])
                city1 = next(x for x in self.Cities if x.id == line[1])
                city2 = next(x for x in self.Cities if x.id == line[2])
                city1.setDestination(conn)
                city2.setDestination(conn)
                self.ticketDeck.cards.append(conn)
