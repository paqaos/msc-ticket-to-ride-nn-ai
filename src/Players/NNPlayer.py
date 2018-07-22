from numpy.random import random

from src.AI import game_data
from src.Enums import DecisionType
from src.Players.AlgoPlayer import AlgoPlayer

train_steps = 3000
batch_size = 100


class NNPlayer(AlgoPlayer):
    def __init__(self, name, game, board, predictor):
        AlgoPlayer.__init__(self, name, game, board)
        self.predictor = predictor

    def calculateDecision(self, game, board, state):

        predict_x = {
            'Turn': [state[0]],
            'PlayerWagonsCards': [state[1]],
            'WagonsBoardHand': [state[2]],
            'WagonsBoardDeck': [state[3]],
            'WagonsBoardGrav': [state[4]],
            'PlayerTickets': [state[5]],
            'BoardTickets': [state[6]],
            'PlayerWagons': [state[7]],
            'PlayerPoints': [state[8]],
            'WagonsOnBoard': [state[9]],
            'PossTracks': [state[10]],
            'MatchTracks': [state[11]],
            'TargetTracks': [state[12]],
            'LackTracks': [state[13]],
            'PlayerCount': [state[14]],
            'MinWagon': [state[15]],
            'MaxWagon': [state[16]],
            'AvgWagon': [state[17]],
            'MedWagon': [state[18]],
            'MinTickets': [state[19]],
            'MaxTickets': [state[20]],
            'AvgTickets': [state[21]],
            'MedTickets': [state[22]],
            'TicketFail': [state[23]],
            'TicketDone': [state[24]],
            'PointsForOthers': [state[25]],
            'MaxColorWagons': [state[26]],
            'DifferentColorWagons': [state[27]]
        }

        classifier = self.predictor.getPredictor()
        predictions = classifier.predict(

            input_fn=lambda: game_data.eval_input_fn(predict_x,

                                                     labels=None,
                                                     batch_size=1))
        for pred in zip(predictions):
            classId= pred[0]['class_ids'][0]
            return DecisionType.DecisionType(classId)
        return DecisionType.DecisionType.PASS
