from src.Players.AlgoPlayer import AlgoPlayer
from src.Board import Board
from src.Enums import DecisionType


class Game:
    def __init__(self):
        self.turn = 1
        self.board = Board()
        self.activePlayer = None
        self.last = False
        self.players = []
        self.playerId = 1

    def prepareGame(self, countAi):
        aiPlayer = AlgoPlayer("cpu#1", self, self.board)
        self.activePlayer = aiPlayer
        self.players.append(aiPlayer)
        for singleAi in range(1, countAi):
            self.players.append(AlgoPlayer('cpu#' + str(singleAi+1), self, self.board))

        if len(self.players) > 3:
            for conn in self.board.Connections:
                conn.double = True

        for player in self.players:
            wagonCards = self.board.wagonsDeck.draw(4)
            player.WagonCards.addCards(wagonCards)
            player.decisionTicket(self.board, self, self.board.ticketDeck.draw(3), 2)

        cards = self.board.wagonsDeck.draw(5)
        self.board.wagonsHand.addCards(cards)

    def execute(self):
        if self.activePlayer is not None:
            while self.activePlayer.Active:
                self.activePlayer.prepareTurn(self.board, self)
                decision = self.activePlayer.calculateDecision(self, self.board)
                if decision == DecisionType.DecisionType.CLAIMTRACK:
                    print(self.activePlayer.PlayerName + 'claim')
                    self.activePlayer.decisionTrack(self.board, self)
                    self.activePlayer.decisions.append(DecisionType.DecisionType.CLAIMTRACK)

                elif decision == DecisionType.DecisionType.TICKETCARD:
                    print(self.activePlayer.PlayerName + 'ticket ' + str(len(self.board.ticketDeck.cards)))
                    self.activePlayer.decisionTicket(self.board, self, self.board.ticketDeck.draw(3), 1)
                    self.activePlayer.decisions.append(DecisionType.DecisionType.TICKETCARD)

                elif decision == DecisionType.DecisionType.WAGONCARD:
                    print(self.activePlayer.PlayerName + 'wagon ' + str(len(self.board.wagonsDeck.cards)) + ' ' + str(len(self.board.wagonsHand.cards)))
                    self.activePlayer.decisionWagons(self.board, self)
                    self.activePlayer.decisions.append(DecisionType.DecisionType.WAGONCARD)

                self.board.refreshHand()
                self.passPlayer()

    def passPlayer(self):
        tmpPlayer = self.activePlayer
        if tmpPlayer.Last:
            tmpPlayer.Last = False
            tmpPlayer.Active = False
        elif not tmpPlayer.Last and tmpPlayer.Wagons <= 2:
            tmpPlayer.Last = True
            self.last = True

        self.players.remove(tmpPlayer)
        self.players.append(tmpPlayer)
        self.activePlayer = self.players[0]

        self.activePlayer.Last = self.last
        if self.activePlayer.Id == 1:
            self.turn += 1

    def printResult(self):
        points = {}
        for pl in self.players:
            points[pl] = pl.calculatePoints(self.board)
            print(pl.PlayerName + ' pts: ' + str(points[pl]))


with open('result_5.csv', 'w') as f, open('done_5.csv', 'w') as tf, open('fail_5.csv', 'w') as ff:
    for pl in range(2, 6):
        for rep in range(250):
            lineTck = ''
            line = ''
            failLine = ''
            myGame = Game()
            myGame.prepareGame(pl)
            myGame.execute()
            myGame.printResult()

            for player in myGame.players:
                line += str(player.Points) + ';'
                failLine += str(player.TicketFail) + ';'
                lineTck += str(player.TicketDone) + ';'

            line += '\n'
            lineTck += '\n'
            failLine += '\n'
            f.write(line)
            tf.write(lineTck)
            ff.write(failLine)
        f.flush()
        tf.flush()
        ff.flush()

