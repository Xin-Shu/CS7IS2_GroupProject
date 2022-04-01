import copy
import datetime
import numpy as np
import tensorflow as tf

sudokuFilePath = '../dataset/sudoku.csv'
lengthData = 100000


def norm(a):
    return (a / 9) - .5


def denorm(a):
    return (a + .5) * 9


def inference_sudoku(model_, sample, if_realGame):

    if if_realGame:
        feat = copy.copy(sample)
        feat = norm(feat)
    else:
        feat = copy.copy(sample)
    while True:

        out = model_.predict(feat.reshape((1, 9, 9, 1)))
        out = out.squeeze()

        pred = np.argmax(out, axis=1).reshape((9, 9)) + 1
        prob = np.around(np.max(out, axis=1).reshape((9, 9)), 2)

        feat = denorm(feat).reshape((9, 9))
        mask = (feat == 0)

        if mask.sum() == 0:
            break

        prob_new = prob * mask

        ind = np.argmax(prob_new)
        x, y = (ind // 9), (ind % 9)

        val = pred[x][y]
        feat[x][y] = val
        feat = norm(feat)

    return pred


def test_accuracy(model_, feats, labels):
    correct = 0

    for i, feat in enumerate(feats):

        pred = inference_sudoku(model_, feat, 0)

        true = labels[i].reshape((9, 9)) + 1

        if abs(true - pred).sum() == 0:
            correct += 1

    return correct / feats.shape[0]


def main():
    import scripts.get_data as get_data
    timeStamp = datetime.datetime.now()
    x_train, x_test, y_train, y_test = get_data.extractCSV(sudokuFilePath, lengthData)
    model = tf.keras.models.load_model('../dataset/trainedDNNModel.h5')
    timeDiffer = datetime.datetime.now() - timeStamp
    print(f'INFO 01: Finished dataset preparation, total time taken: {timeDiffer}.')

    numOfGames = 1000
    imeStamp = datetime.datetime.now()
    avgAccuracy = test_accuracy(model, x_test[:numOfGames], y_test[:numOfGames])
    timeDiffer = datetime.datetime.now() - timeStamp
    print(f'INFO 02: Finished {numOfGames} games, total time taken: {timeDiffer}, '
          f'avg. time per game: {(timeDiffer / numOfGames).microseconds} msecs, avg. accuracy: {avgAccuracy}')


if __name__ == '__main__':
    main()
