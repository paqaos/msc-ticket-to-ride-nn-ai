import os
import sys
from datetime import datetime

from src.Helpers.StatePrint import StatePrint
from src.Players.AlgoPlayer import AlgoPlayer
from src.Board import Board
from src.Enums import DecisionType
import uuid
import csv
import tensorflow as tf

from src.Players.DecisionNNPredictor import DecisionNNPredictor
from src.Players.NNPlayer import NNPlayer


class Game:
    def __init__(self):
        self.gameId = uuid.uuid4()
        self.turn = 1
        self.board = Board()
        self.activePlayer = None
        self.last = False
        self.players = []
        self.playerId = 1

    def prepareGame(self, countAi, predictor):
        aiPlayer = NNPlayer("cpu#1", self, self.board, predictor)
        self.activePlayer = aiPlayer
        self.players.append(aiPlayer)
        for singleAi in range(1, countAi):
            self.players.append(NNPlayer('cpu#' + str(singleAi+1), self, self.board, predictor))

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
                print('new player' + str(self.turn))
                self.activePlayer.prepareTurn(self.board, self)
                self.activePlayer.calculatePoints(self.board)
                state = StatePrint.printState(self, self.activePlayer)
                decision = self.activePlayer.calculateDecision(self, self.board,state)
                if decision == DecisionType.DecisionType.CLAIMTRACK:
                    self.activePlayer.decisionTrack(self.board, self)
                    self.activePlayer.decisions.append(DecisionType.DecisionType.CLAIMTRACK)

                elif decision == DecisionType.DecisionType.TICKETCARD:
                    self.activePlayer.decisionTicket(self.board, self, self.board.ticketDeck.draw(3), 1)
                    self.activePlayer.decisions.append(DecisionType.DecisionType.TICKETCARD)

                elif decision == DecisionType.DecisionType.WAGONCARD:
                    self.activePlayer.decisionWagons(self.board, self)
                    self.activePlayer.decisions.append(DecisionType.DecisionType.WAGONCARD)

                state.append(decision.value)
                #  with open('reports/' + str(self.gameId) + '/' + str(self.activePlayer.PlayerName) + '.sth', 'a', newline='') as stateFile:
                #    csvWr = csv.writer(stateFile)
                #    csvWr.writerow(state)

                #  self.activePlayer.decisions.append(state)

                del state
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


startAll = datetime.utcnow()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
preserveGameLog = False

with tf.device('/device:GPU:0'):
    tf.logging.set_verbosity(tf.logging.ERROR)
    with open('result_10nn3pl.csv', 'w') as f, open('done_10nn3pl.csv', 'w') as tf, open('fail_10nn3pl.csv', 'w') as ff:
        predictor = DecisionNNPredictor()
        for pl in range(2, 5):
            for rep in range(200):
                startDate = datetime.utcnow()
                lineTck = ''
                line = ''
                failLine = ''
                myGame = Game()
                if not os.path.exists('reports/'):
                    os.makedirs('reports')
                os.makedirs('reports/' + str(myGame.gameId))

                try:
                    myGame.prepareGame(pl, predictor)
                    myGame.execute()
                    myGame.printResult()
                    line += str(myGame.gameId) +';'
                    with open('reports/' + str(myGame.gameId) + '/raport.txt', 'w') as report:
                        for player in myGame.players:
                            line += str(player.Points) + ';'
                            report.write(str(player.PlayerName) + ' ' + str(player.Points))
                            failLine += str(player.TicketFail) + ';'
                            lineTck += str(player.TicketDone) + ';'
                except:
                    e = sys.exc_info()[0]
                    line += 'fail' + str(len(myGame.players))
                    failLine += 'fail' + str(len(myGame.players))
                    lineTck += 'fail' + str(len(myGame.players))

                line += '\n'
                lineTck += '\n'
                failLine += '\n'
                f.write(line)
                tf.write(lineTck)
                ff.write(failLine)
                endDate = datetime.utcnow()
                print('start exp: ' + str(startDate) + ' end date: ' + str(endDate))
                f.flush()
                tf.flush()
                ff.flush()
                del myGame

endall = datetime.utcnow()

print('start ' + str(startAll))
print('end ' +  str(endall))