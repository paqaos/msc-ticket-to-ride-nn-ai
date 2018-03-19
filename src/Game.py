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
        for player in self.players:
            wagonCards = self.board.wagonsDeck.draw(4)
            player.WagonCards.addCards(wagonCards)

            ticketCards = self.board.ticketDeck.draw(3)
            returned = player.drawTickets(2, ticketCards)
            self.board.ticketDeck.addCards(returned)

    def execute(self):
        if self.activePlayer is not None:
            while self.activePlayer.Active or self.activePlayer.Last:
                decision = self.activePlayer.calculateDecision(self.board)
                if decision == DecisionType.DecisionType.CLAIMTRACK:
                    self.activePlayer.ClaimTrack(self.board)
                elif decision == DecisionType.DecisionType.TICKETCARD:
                    self.activePlayer.DrawTickets(self.board, 1, self.board.ticketDeck.draw(3))
                else:
                    self.activePlayer.DrawWagons(None, self.board.wagonsDeck, 2)
                self.passPlayer()

    def passPlayer(self):
        tmpPlayer = self.activePlayer
        self.players.remove(tmpPlayer)
        self.players.append(tmpPlayer)
        self.activePlayer = self.players[0]


myGame = Game()
myGame.prepareGame()
# myGame.execute()
