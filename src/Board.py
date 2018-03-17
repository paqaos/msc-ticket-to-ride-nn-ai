import random
import csv

from src.Cards.WagonCard import WagonCard
from src.Collections.Deck import Deck
from src.Enums import Colors
from src.Map.City import City
from src.Map.Connection import Connection


class Board:
    Cities = []
    Connections = []

    def __init__(self):
        self.wagonsDeck = Deck()
        self.ticketDeck = Deck()
        self.wagonGraveyard = Deck()
        self.__prepareCards__()
        self.__prepareMap__()

    def __prepareCards__(self):
        for color in Colors.Colors:
            for i in range(12):
                card = WagonCard(color)
                self.wagonsDeck.add(card)

        for i in range(2):
            self.wagonsDeck.add(WagonCard(Colors.Colors.Rainbow))

        random.shuffle(self.wagonsDeck.cards)

    def __prepareMap__(self):

        with open("data/usa/cities.csv", 'rt') as f:
            reader = csv.reader(f, delimiter=';')

            for line in reader:
                self.Cities.append(City(line[0], line[1]))

        with open("data/usa/connections.csv", 'rt') as f:
            reader = csv.reader(f, delimiter=';')

            for line in reader:
                conn = Connection(line[0], line[1], line[2], [])
                city1 = next(x for x in self.Cities if x.id == line[3])
                city2 = next(x for x in self.Cities if x.id == line[4])
                print city1.name + ' -> ' + city2.name
                city1.setConnection(conn)
                city2.setConnection(conn)
                self.Connections.append(conn)
