from src.Board import Board


class Game:
    def __init__(self):
        self.turn = 0
        self.board = Board()
        self.players = []
        self.activePlayer = None

    def prepareGame(self):
        pass

    def execute(self):
        pass


myGame = Game()
myGame.prepareGame()
myGame.execute()
