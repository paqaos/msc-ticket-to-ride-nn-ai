from numpy.random import random

from src.AI import game_data
from src.Enums import DecisionType
from src.Players.AlgoPlayer import AlgoPlayer
import tensorflow as tf

train_steps = 1000
batch_size = 100

class NNPlayer(AlgoPlayer):
    def __init__(self, name, game, board):
        AlgoPlayer.__init__(self, name, game, board)

        (train_x, train_y) = game_data.load_data(path='dataset/learn.csv')

        my_feature_columns = []
        for key in train_x.keys():
            my_feature_columns.append(tf.feature_column.numeric_column(key=key))

        self.classifier = tf.estimator.DNNClassifier(
            feature_columns=my_feature_columns,
            hidden_units=[60, 60],
            n_classes=5
        )

        self.classifier.train(
            input_fn=lambda: game_data.train_input_fn(train_x,
                                                      train_y,
                                                      batch_size),
            steps=train_steps)

    def calculateDecision(self, game, board, state):

        predict_x = {
            'PLAYER_ID': [state[0]],
            'TURN': [state[1]],
            'CARAIN': [state[2]],
            'CARED': [state[3]],
            'CABLUE': [state[4]],
            'CAWHI': [state[5]],
            'CABLA': [state[6]],
            'CAGRE': [state[7]],
            'CAPIN': [state[8]],
            'CAORA': [state[9]],
            'CAYEL': [state[10]],
            'WAGONHAND': [state[11]],
            'WAGONDECK': [state[12]],
            'WAGONGRAV': [state[13]],
            'TICKETS': [state[14]],
            'TICKETDECK': [state[15]],
            'WAGONS': [state[16]],
            'POINTS': [state[17]],
            'POSS': [state[18]],
            'MATCH': [state[19]],
            'TARGETS': [state[20]],
            'LACK': [state[21]],
            'PLAYERS': [state[22]],
            'MINPTS': [state[23]],
            'MAXPTS': [state[24]],
            'AVGPTS': [state[25]],
            'MEDPTS': [state[26]],
            'MINWGN': [state[27]],
            'MAXWGN': [state[28]],
            'AVGWGN': [state[29]],
            'MEDWGN': [state[30]],
            'MITTCK': [state[31]],
            'MAXTCK': [state[32]],
            'AVGTCK': [state[33]],
            'MEDTCK': [state[34]],
            'MINWGC': [state[35]],
            'MAXWGC': [state[36]],
            'AVGWGC': [state[37]],
            'MEDWGC': [state[38]]
        }

        predictions = self.classifier.predict(

            input_fn=lambda: game_data.eval_input_fn(predict_x,

                                                     labels=None,

                                                     batch_size=batch_size))
        for pred in zip(predictions):
            classId= pred[0]['class_ids'][0]
            return DecisionType.DecisionType(classId)
        return DecisionType.DecisionType.PASS
