import pandas as pd
import tensorflow as tf

CSV_TYPES = [
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0]
]
CSV_COLUMN_NAMES = [
    'PLAYER_ID',
    'TURN',
    'CARAIN',
    'CARED',
    'CABLUE',
    'CAWHI',
    'CABLA',
    'CAGRE',
    'CAPIN',
    'CAORA',
    'CAYEL',
    'WAGONHAND',
    'WAGONDECK',
    'WAGONGRAV',
    'TICKETS',
    'TICKETDECK',
    'WAGONS',
    'POINTS',
    'POSS',
    'MATCH',
    'TARGETS',
    'LACK',
    'PLAYERS',
    'MINPTS',
    'MAXPTS',
    'AVGPTS',
    'MEDPTS',
    'MINWGN',
    'MAXWGN',
    'AVGWGN',
    'MEDWGN',
    'MITTCK',
    'MAXTCK',
    'AVGTCK',
    'MEDTCK',
    'MINWGC',
    'MAXWGC',
    'AVGWGC',
    'MEDWGC',
    'Decision'
]

Decisions = [
    'START',
    'WAGON',
    'TICKET',
    'TRACK',
    'PASS'
]

def load_data(y_name='Decision', path='../dataset/learn.csv'):
    train_path = path #tf.keras.utils.get_file('file://../dataset/learn.csv', 'file://../dataset')

    train = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0, delimiter=',')
    train_x, train_y = train, train.pop(y_name)

    return (train_x, train_y)

def train_input_fn(features, labels, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)

    return dataset

def eval_input_fn(features, labels, batch_size):
    features = dict(features)
    if labels is None:
        inputs = features
    else:
        inputs = (features, labels)

    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    assert batch_size is not None, "batch must not be None"
    dataset = dataset.batch(batch_size)

    return dataset

def _parse_line(line):
    fields = tf.decode_csv(line, record_defaults=CSV_TYPES)

    features = dict(zip(CSV_COLUMN_NAMES, fields))

    label = features.pop('Decision')

    return features, label

def csv_input_fn(csv_path, batch_size):
    dataset = tf.data.TextLineDataset(csv_path)

    dataset = dataset.map(_parse_line)

    dataset = dataset.shuffle(1000).repeat().batch(batch_size)

    return dataset