from enum import Enum


class Colors(Enum):
    Rainbow = 0
    Red = 1
    Blue = 2
    White = 3
    Black = 4
    Green = 5
    Pink = 6
    Orange = 7
    Yellow = 8

    @staticmethod
    def fromString(content):
        if content == '0':
            return Colors.Rainbow
        if content == '1':
            return Colors.Red
        if content == '2':
            return Colors.Blue
        if content == '3':
            return Colors.White
        if content == '4':
            return Colors.Black
        if content == '5':
            return Colors.Green
        if content == '6':
            return Colors.Pink
        if content == '7':
            return Colors.Orange
        if content == '8':
            return Colors.Yellow
        return None
