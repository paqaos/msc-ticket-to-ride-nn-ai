import csv
import os
import sys
from datetime import datetime
from subprocess import call
import tensorflow as tf

from src.Logic.Game import Game
from src.Players.DecisionNNPredictor import DecisionNNPredictor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
preserveGameLog = False

from src.AI import game_data


class Experiment:
    def __init__(self, modelPath, experimentName, gamesPerConf, source, tf ):
        self.modelPath = modelPath
        self.predictor = DecisionNNPredictor(modelPath)
        (train_x, train_y) = game_data.load_data(path=source)

        self.my_feature_columns = []
        for key in train_x.keys():
            self.my_feature_columns.append(tf.feature_column.numeric_column(key=key))

        self.my_config = tf.estimator.RunConfig(
            save_checkpoints_secs=20 * 60,
            keep_checkpoint_max=5
        )

        self.train_x = train_x
        self.train_y = train_y
        self.evaluate = None

        self.directory = 'GameResults'
        self.experimentName = experimentName
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.experimentPath = self.directory + '/' + experimentName

        if not os.path.exists(self.experimentPath):
            os.makedirs(self.experimentPath)

        self.games = gamesPerConf
        self.tf = tf

    def make_iteration(self, iteration, playerStart = 2, playerEnd = 5):
        iteration_result = { }
        localPath = self.experimentPath + '/' + str(iteration)
        if not os.path.exists(localPath):
            os.makedirs(localPath)

        self.tf.logging.set_verbosity(self.tf.logging.ERROR)
        fileResult = self.experimentPath + '/' + str(iteration) + '/result.csv'
        fileDone = self.experimentPath + '/' + str(iteration) + '/done.csv'
        fileFail = self.experimentPath + '/' + str(iteration) + '/fail.csv'

        fails = 0
        games = 0
        max_pts = 0
        min_pts = 200
        sum_turns = 0
        sum_points = 0
        players = 0
        finished = 0
        with open(fileResult, 'w') as fr, open(fileDone, 'w') as fd, open(fileFail, 'w') as ff:
            predictor = self.predictor.getPredictor()
            for pl in range(playerStart, playerEnd):
                for rep in range(self.games):
                    games += 1
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
                        line += str(myGame.gameId) + ';'
                        with open('reports/' + str(myGame.gameId) + '/raport.txt', 'w') as report:
                            finished += 1
                            sum_turns += myGame.turn
                            for player in myGame.players:
                                if player.Points > max_pts:
                                    max_pts = player.Points
                                if player.Points < min_pts:
                                    min_pts = player.Points
                                sum_points += player.Points
                                players += 1
                                line += str(player.Points) + ';'
                                report.write(str(player.PlayerName) + ' ' + str(player.Points))
                                failLine += str(player.TicketFail) + ';'
                                lineTck += str(player.TicketDone) + ';'
                    except:
                        e = sys.exc_info()[0]
                        print(e)
                        fails += 1
                        line += 'fail ' + str(len(myGame.players)) + ' in turn: ' + str(myGame.turn)
                        failLine += 'fail ' + str(len(myGame.players)) + ' in turn: ' + str(myGame.turn)
                        lineTck += 'fail ' + str(len(myGame.players)) + ' in turn: ' + str(myGame.turn)
                        sum_turns += myGame.turn

                    line += '\n'
                    lineTck += '\n'
                    failLine += '\n'
                    fr.write(line)
                    fd.write(lineTck)
                    ff.write(failLine)
                    fr.flush()
                    fd.flush()
                    ff.flush()
                    del myGame
        iteration_result['games'] = games
        iteration_result['fails'] = fails

        if finished == 0:
            min = '-'
            max = '-'

        iteration_result['max'] = max_pts
        iteration_result['min'] = min_pts

        iteration_result['players'] = players
        iteration_result['finished'] = finished
        if players == 0:
            iteration_result['avg'] = '-'
        else:
            iteration_result['avg'] = sum_points / players
        iteration_result['turns'] = sum_turns / games

        return iteration_result

    def make_learning(self, batch_size):
        self.predictor.getPredictor().train(
            input_fn=lambda: game_data.train_input_fn(self.train_x,
                                                      self.train_y,
                                                      batch_size),
            steps=batch_size)

    def make_evaluate(self, batch_size):
        tf.contrib.summary.eval_dir(self.experimentPath)

        if not os.path.exists(modelPath):
            os.makedirs(modelPath)
            os.makedirs(modelPath+'/eval')
        eval_result = self.predictor.getPredictor().evaluate(
            input_fn=lambda: game_data.eval_input_fn(self.train_x,
                                                     self.train_y,
                                                     batch_size),
            steps=batch_size)

        return eval_result

    def run_experiment(self, learn_iteration, learn_batch, with_learn, start_iteration=1, epochs = 1, playerStart = 2, playerEnd = 5, skipFirst = False):
        with open(self.experimentPath + '/experiment.txt', 'a') as log, open(self.experimentPath + '/experiment.csv', 'a', newline='' ) as qualityf :
            experiment_start = datetime.utcnow()
            log.write('experiment started: ' + str(experiment_start) + '\n')
            for li in range(start_iteration, learn_iteration+1):
                log.write('iteration ' + str(li) + ' started: ' + str(datetime.utcnow()) + '\n')
                if with_learn and not (skipFirst and li == start_iteration):
                    for i in range(epochs):
                        print('learn epoch: ' + str(i))
                        self.make_learning(learn_batch)
                quality = self.make_evaluate(learn_batch)
                iteration_quality = self.make_iteration(li, playerStart, playerEnd+1)
                print('step' + str(li))
                log.write('iteration ' + str(li) + ' ended: ' + str(datetime.utcnow()) + '\n')
                log.flush()

                qualityOut = []
                qualityOut.append(li)
                qualityOut.append(quality['global_step'])
                qualityOut.append(quality['loss'])
                qualityOut.append(quality['average_loss'])
                qualityOut.append(quality['accuracy'])

                qualityOut.append(iteration_quality['games'])
                qualityOut.append(iteration_quality['fails'])
                qualityOut.append(iteration_quality['max'])
                qualityOut.append(iteration_quality['min'])
                qualityOut.append(iteration_quality['players'])
                qualityOut.append(iteration_quality['finished'])
                qualityOut.append(iteration_quality['avg'])
                qualityOut.append(iteration_quality['turns'])
                csvWr = csv.writer(qualityf)
                csvWr.writerow(qualityOut)
                qualityf.flush()
            experiment_end = datetime.utcnow()
            log.write('experiment ended: ' + str(experiment_end) + '\n')
            log.flush()


if __name__ == '__main__':

    learn_batch = 100
    learn_iteration = 10

    modelPath = 'models/poc2'
    source = 'dataset/learn_all.csv'

    experiment = Experiment(modelPath, 'proove', 60, source, tf)
    experiment.run_experiment(learn_iteration, learn_batch, True, start_iteration=9, epochs=1, playerEnd=5, playerStart=2, skipFirst=False)