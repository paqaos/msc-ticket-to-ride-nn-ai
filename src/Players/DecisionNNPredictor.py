import tensorflow as tf
from src.AI import game_data


class DecisionNNPredictor:
    def __init__(self):
        (train_x, train_y) = game_data.load_data(path='dataset/learn.csv')

        my_feature_columns = []
        for key in train_x.keys():
            my_feature_columns.append(tf.feature_column.numeric_column(key=key))

        self.classifier = tf.estimator.DNNClassifier(
                feature_columns=my_feature_columns,
                hidden_units=[180, 160],
                n_classes=5,
                model_dir='models/decision'
            )

    def getPredictor(self):
        return self.classifier
