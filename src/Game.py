from src.Players.AlgoPlayer import AlgoPlayer
from src.Board import Board
from src.Enums import DecisionType
from src.Players.HumanPlayer import HumanPlayer


class Game:
    def __init__(self):
        self.turn = 0
        self.board = Board()
        self.players = []
        self.activePlayer = None

    def prepareGame(self):
        aiPlayer = HumanPlayer("cpu#1", self, self.board)
        self.activePlayer = aiPlayer
        self.players.append(aiPlayer)
        # self.players.append(AlgoPlayer("cpu#2", self, self.board))
        for player in self.players:
            wagonCards = self.board.wagonsDeck.draw(4)
            player.WagonCards.addCards(wagonCards)

            self.activePlayer.decisionTicket(self.board, self, self.board.ticketDeck.draw(3), 2)

        cards = self.board.wagonsDeck.draw(5)
        self.board.wagonsHand.addCards(cards)

    def execute(self):
        if self.activePlayer is not None:
            while self.activePlayer.Active or self.activePlayer.Last:
                decision = self.activePlayer.calculateDecision(self, self.board)
                if decision == DecisionType.DecisionType.CLAIMTRACK:
                    print self.activePlayer.PlayerName + 'claim'
                    self.activePlayer.ClaimTrack(self.board)
                elif decision == DecisionType.DecisionType.TICKETCARD:
                    print self.activePlayer.PlayerName + 'ticket'
                    self.activePlayer.decisionTicket(self.board, self, self.board.ticketDeck.draw(3), 1)
                else:
                    print self.activePlayer.PlayerName + 'wagon'
                    self.activePlayer.decisionWagons(self.board, self)
                self.board.refreshHand()
                self.passPlayer()

    def passPlayer(self):
        tmpPlayer = self.activePlayer
        self.players.remove(tmpPlayer)
        self.players.append(tmpPlayer)
        self.activePlayer = self.players[0]

    def drawWagon(self, player, card):
        pass

myGame = Game()
myGame.prepareGame()
myGame.execute()
