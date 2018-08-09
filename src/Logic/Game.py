from src.Helpers.StatePrint import StatePrint
from src.Logic.Board import Board
from src.Enums import DecisionType
import uuid

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
                elif decision == DecisionType.DecisionType.START:
                    raise RuntimeError('Cannot use start decision')
                elif decision == DecisionType.DecisionType.PASS:
                    canDrawWagons = len(self.board.wagonsDeck.cards) > 0 or len(self.board.wagonsHand.cards) > 0
                    canClaim = len(self.activePlayer.__poss__) > 0
                    canTicket = len(self.board.ticketDeck) > 0
                    if canDrawWagons or canClaim or canTicket:
                        raise RuntimeError('User cannot skip turn')

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
