import os
import sys
from datetime import datetime
import tensorflow as tf

from src.Logic.Game import Game
from src.Players.DecisionNNPredictor import DecisionNNPredictor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
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

        self.directory = 'GameResults'
        self.experimentName = experimentName
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.experimentPath = self.directory + '/' + experimentName

        if not os.path.exists(self.experimentPath):
            os.makedirs(self.experimentPath)

        self.games = gamesPerConf
        self.tf = tf

    def make_iteration(self, iteration):
        with self.tf.device('/device:GPU:0'):
            localPath = self.experimentPath + '/' + str(iteration)
            if not os.path.exists(localPath):
                os.makedirs(localPath)

            self.tf.logging.set_verbosity(self.tf.logging.ERROR)
            fileResult = self.experimentPath + '/' + str(iteration) + '/result.csv'
            fileDone = self.experimentPath + '/' + str(iteration) + '/done.csv'
            fileFail = self.experimentPath + '/' + str(iteration) + '/fail.csv'

            with open(fileResult, 'w') as fr, open(fileDone, 'w') as fd, open(fileFail, 'w') as ff:
                predictor = DecisionNNPredictor(modelPath)
                for pl in range(2, 6):
                    fails = 0
                    for rep in range(self.games):
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
                                for player in myGame.players:
                                    line += str(player.Points) + ';'
                                    report.write(str(player.PlayerName) + ' ' + str(player.Points))
                                    failLine += str(player.TicketFail) + ';'
                                    lineTck += str(player.TicketDone) + ';'
                        except:
                            e = sys.exc_info()[0]
                            fails += 1
                            line += 'fail ' + str(len(myGame.players)) + ' in turn: ' + str(myGame.turn)
                            failLine += 'fail ' + str(len(myGame.players)) + ' in turn: ' + str(myGame.turn)
                            lineTck += 'fail ' + str(len(myGame.players)) + ' in turn: ' + str(myGame.turn)

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

    def make_learning(self, batch_size):
        self.predictor.getPredictor().train(
            input_fn=lambda: game_data.train_input_fn(self.train_x,
                                                      self.train_y,
                                                      batch_size),
            steps=batch_size)

    def run_experiment(self, learn_iteration, learn_batch, with_learn):
        with open(self.experimentPath + '/experiment.txt', 'w') as log:
            experiment_start = datetime.utcnow()
            log.write('experiment started: ' + str(experiment_start) + '\n')
            for li in range(1, learn_iteration+1):
                log.write('iteration ' + str(li) + ' started: ' + str(datetime.utcnow()) + '\n')
                if with_learn and li != 1:
                    self.make_learning(learn_batch)
                self.make_iteration(li)
                print('step' + str(li))
                log.write('iteration ' + str(li) + ' ended: ' + str(datetime.utcnow()) + '\n')
                log.flush()
            experiment_end = datetime.utcnow()
            log.write('experiment ended: ' + str(experiment_end) + '\n')
            log.flush()


if __name__ == '__main__':
    learn_iteration = 10
    learn_batch = 100
    modelPath = 'models/proove'
    source = 'dataset/learn.csv'

    experiment = Experiment(modelPath, 'exp1', 1, source, tf)
    experiment.run_experiment(learn_iteration, learn_batch, True)
