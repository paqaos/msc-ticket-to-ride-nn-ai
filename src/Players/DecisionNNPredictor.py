import tensorflow as tf
from src.AI import game_data


class DecisionNNPredictor:
    def __init__(self):
        (train_x, train_y) = game_data.load_data(path='dataset/learn.csv')
        self.train_x = train_x
        self.train_y = train_y

        self.my_feature_columns = []
        for key in train_x.keys():
            self.my_feature_columns.append(tf.feature_column.numeric_column(key=key))

        self.gpu_config = tf.GPUOptions(allow_growth=True)
        self.my_session = tf.ConfigProto(log_device_placement=False, gpu_options=self.gpu_config)
        self.my_config = tf.estimator.RunConfig(
            session_config=self.my_session
        )

    def getPredictor(self):
        classifier = tf.estimator.DNNClassifier(
                feature_columns=self.my_feature_columns,
                hidden_units=[180, 160],
                n_classes=5,
                model_dir='models/decision',
                config=self.my_config
            )
        return classifier
