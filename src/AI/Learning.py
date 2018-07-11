from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

import game_data

train_steps = 1000
batch_size = 100


def main(argv):
    (train_x, train_y) = game_data.load_data()

    my_feature_columns = []
    for key in train_x.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))

    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        hidden_units=[60,60],
        n_classes=5
    )


    classifier.train(
        input_fn=lambda:game_data.train_input_fn(train_x,
                                                 train_y,
                                                 batch_size),
            steps=train_steps)

if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)