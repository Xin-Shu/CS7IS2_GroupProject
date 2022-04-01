import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def extractCSV(file, numOfGames):

    data = pd.read_csv(file)

    feat_raw = data.iloc[:, 0]
    label_raw = data.iloc[:, 1]
    if numOfGames > len(feat_raw):
        print(f'Warning 01: Requested number of games is {numOfGames}, while the length of dataset is {len(feat_raw)}')
        numOfGames = len(feat_raw)

    feat = []
    label = []

    for i in feat_raw[:numOfGames]:

        x = np.array([int(j) for j in i]).reshape((9, 9, 1))
        feat.append(x)

    feat = np.array(feat)
    feat = feat / 9
    feat -= 0.5

    for i in label_raw[:numOfGames]:

        x = np.array([int(j) for j in i]).reshape((81, 1)) - 1
        label.append(x)

    label = np.array(label)

    x_train, x_test, y_train, y_test = train_test_split(feat, label, test_size=0.2, random_state=42)

    del feat_raw
    del label_raw

    return x_train, x_test, y_train, y_test


extractCSV('../dataset/sudoku.csv', 2)
