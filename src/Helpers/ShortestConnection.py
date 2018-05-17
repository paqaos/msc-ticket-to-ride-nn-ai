class ShortestConnection:
    @staticmethod
    def calculatePath(board, player, source, target):
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
                if conn.cities[0].id != minCity.inner.id:
                    otherCity = conn.cities[0]
                else:
                    otherCity = conn.cities[1]

                exists = False
                for city in cities:
                    if city.inner.id == otherCity.id:
                        exists = True

                if not exists:
                    continue

                for x in cities:
                    if x.inner.id == otherCity.id:
                        actual = x

                alt = int(minCity.cost) + int(conn.getCost(player))
                if alt < actual.cost:
                    actual.cost = alt
                    actual.previous = minCity
                    actual.conn = conn

        if found and minCity.cost < float("inf"):
            actual = minCity
            while actual is not None and actual.conn is not None:
                result.insert(0, actual.conn)
                actual = actual.previous
            return result

        return None


class CityTarget:
    def __init__(self, inner):
        self.cost = float("inf")
        self.inner = inner
        self.previous = None
        self.conn = None