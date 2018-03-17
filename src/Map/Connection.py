class Connection:
    owner = None

    def __init__(self, id, size, color, cities):
        self.size = size
        self.color = color
        self.cities = cities
        self.id = id
