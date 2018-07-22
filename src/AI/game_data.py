import pandas as pd
import tensorflow as tf

CSV_TYPES = [
    [0],  # Turn
    [0],  # Player wagons
    [0],  # Board wagons hand
    [0],  # Board wagons deck
    [0],  # Board wagons grav
    [0],  # Player Tickets
    [0],  # Board tickets
    [0],  # Player wagons
    [0],  # Player Points

    [0],  # Wagons on board

    [0],  # Player poss tracks
    [0],  # Player match tracks
    [0],  # Target tracks
    [0],  # Lack tracks
    [0],  # Players count

    [0],  # min wagon
    [0],  # max wagon
    [0.0],  # avg wagons
    [0.0],  # median wagons

    [0],  # max tickets
    [0],  # min tickets
    [0.0],  # avg tickets
    [0.0],  # med tickets

    [0],  # ticket fail
    [0],  # ticket done
    [0],  # points for others

    [0],  # Max single color
    [0],  # Different color cards

    [0]  # Decision
]
CSV_COLUMN_NAMES = [
    'Turn',
    'PlayerWagonsCards',
    'WagonsBoardHand',
    'WagonsBoardDeck',
    'WagonsBoardGrav',
    'PlayerTickets',
    'BoardTickets',
    'PlayerWagons',
    'PlayerPoints',
    'WagonsOnBoard',
    'PossTracks',
    'MatchTracks',
    'TargetTracks',
    'LackTracks',
    'PlayerCount',
    'MinWagon',
    'MaxWagon',
    'AvgWagon',
    'MedWagon',
    'MinTickets',
    'MaxTickets',
    'AvgTickets',
    'MedTickets',
    'TicketFail',
    'TicketDone',
    'PointsForOthers',
    'MaxColorWagons',
    'DifferentColorWagons',
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
    train_path = path

    train = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0, delimiter=',')
    train_x, train_y = train, train.pop(y_name)

    return train_x, train_y


def train_input_fn(features, labels, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels)).shuffle(5000).repeat().batch(batch_size)

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
    dataset = tf.data.TextLineDataset(csv_path).map(_parse_line)

    return dataset.shuffle(5000).repeat().batch(batch_size)
