import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def extractCSV(file, numOfGames):

    data = pd.read_csv(file)

    feat_raw = data.iloc[:, 0]
    label_raw = data.iloc[:, 1]

    feat = []
    label = []

    for i in feat_raw[:numOfGames]:

        x = np.array([int(j) for j in i]).reshape((9,9,1))
        feat.append(x)

    feat = np.array(feat)
    feat = feat/9
    feat -= .5

    for i in label_raw[:numOfGames]:

        x = np.array([int(j) for j in i]).reshape((81,1)) - 1
        label.append(x)

    label = np.array(label)

    del feat_raw
    del label_raw

    x_train, x_test, y_train, y_test = train_test_split(feat, label, test_size=0.2, random_state=42)

    print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

    return x_train, x_test, y_train, y_test


if __name__ == '__main__':
    extractCSV('../dataset/sudoku.csv')
