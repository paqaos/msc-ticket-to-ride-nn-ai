import sys


class ShortestPath:
    def __init__(self):
        pass

    @staticmethod
    def calculate(board, player, source, target):
        cities = []
        result = []
        found = False
        for city in board.Cities:
            tmpCity = CityTarget(city)
            cities.append(tmpCity)

        for i in cities:
            if i.inner == source:
                i.cost = 0

        while len(cities) > 0:
            minCity = cities[0]
            for city in cities:
                if city.cost < minCity.cost:
                    minCity = city

            cities.remove(minCity)

            if minCity.inner == target:
                found = True
                break

            for conn in minCity.inner.Connections:
                if conn.cities[0] != minCity.inner:
                    otherCity = conn.cities[0]
                else:
                    otherCity = conn.cities[1]

                for x in cities:
                    if x.inner == otherCity:
                        actual = x

                alt = int(minCity.cost) + int(conn.getCost(player))
                if alt < actual.cost:
                    actual.cost = alt
                    actual.prev = minCity

        if found and minCity.cost < float("inf"):
            actual = minCity
            while actual.inner != source:
                result.insert(0, actual)
                actual = actual.prev
            result.insert(0, actual)
            return result

        return None


class CityTarget:
    def __init__(self, inner):
        self.cost = float("inf")
        self.inner = inner
        self.previous = None
