from src import Player
from src.AlgoPlayer import AlgoPlayer
from src.Board import Board
from src.Enums import DecisionType


class Game:
    def __init__(self):
        self.turn = 0
        self.board = Board()
        self.players = []
        self.activePlayer = None

    def prepareGame(self):
        aiPlayer = AlgoPlayer("cpu#1")
        self.activePlayer = aiPlayer
        self.players.append(aiPlayer)
        self.players.append(AlgoPlayer("cpu#2"))
        for a in self.board.wagonsDeck.cards:
            print(a)
        print(self.board.wagonsDeck.cards)

    def execute(self):
        if self.activePlayer is not None:
            while self.activePlayer.Active or self.activePlayer.Last:
                decision = self.activePlayer.calculateDecision(self.board)
                if decision == DecisionType.DecisionType.CLAIMTRACK:
                    self.activePlayer.ClaimTrack(self.board)
                self.passPlayer()

    def passPlayer(self):
        tmpPlayer = self.activePlayer
        self.players.remove(tmpPlayer)
        self.players.append(tmpPlayer)
        self.activePlayer = self.players[0]
        print self.activePlayer.PlayerName

myGame = Game()
myGame.prepareGame()
myGame.execute()
