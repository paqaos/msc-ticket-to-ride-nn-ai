class DistancePointCalculator:
    @staticmethod
    def calculatePoints(length):
        if length == 1:
            return 1
        if length == 2:
            return 2
        if length == 3:
            return 4
        if length == 4:
            return 7
        if length == 5:
            return 10
        if length == 6:
            return 15