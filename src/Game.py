from src.Board import Board


class Game:
    def __init__(self):
        self.turn = 0
        self.board = Board()
        self.players = []
        self.activePlayer = None

    def prepareGame(self):
        for a in self.board.wagonsDeck.cards:
            print(a)
        print(self.board.wagonsDeck.cards)

    def execute(self):
        pass


myGame = Game()
myGame.prepareGame()
myGame.execute()
