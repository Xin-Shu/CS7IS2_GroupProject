import sys
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import date

dataPath = '../dataset/sudoku.csv'


def extractCSV(path):
    __x, __y = [], []
    cvs = pd.read_csv(path)
    x_colum1 = cvs.iloc[:, 0]       # 81 digits of given SUDOKU puzzle (input)
    x_colum2 = cvs.iloc[:, 1]       # 81 digits of solved SUDOKU puzzle (output)

    for j in tqdm(range(0, len(x_colum1)), bar_format='{percentage:3.0f}%|{bar:100}{r_bar}'):
        numSeries = int(x_colum1[j])
        tempArr = []
        for i in reversed(range(0, 81)):
            currentDigit = numSeries // 10 ** i % 10
            tempArr.append(currentDigit)
        __x.append(tempArr)

    for j in tqdm(range(0, len(x_colum2)), bar_format='{percentage:3.0f}%|{bar:100}{r_bar}'):
        numSeries = int(x_colum2[j])
        tempArr = []
        for i in reversed(range(0, 81)):
            currentDigit = numSeries // 10 ** i % 10
            tempArr.append(currentDigit)
        __y.append(tempArr)

    return __x, __y


if __name__ == '__main__':
    x, y = extractCSV(dataPath)
    print(len(x), len(x[0]))
    print(len(y), len(y[0]))
    x, y = np.array(x), np.array(y)
    pd.DataFrame(x).to_csv('/users/ugrad/xins/Desktop/CS7IS2/CS7IS2_GroupProject/dataset/input.csv')
    pd.DataFrame(y).to_csv('/users/ugrad/xins/Desktop/CS7IS2/CS7IS2_GroupProject/dataset/output.csv')


