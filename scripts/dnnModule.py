import sys
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import date


inputFilePath = '../dataset/input.csv'
outputFilePath = '../dataset/output.csv'


def extractCSV(inputPath, outputPath):
    inputArr, outputArr = [], []
    inputFile = pd.read_csv(inputPath)
    outputFile = pd.read_csv(outputPath)

    count = 0
    while count <= 100:
        x_in = inputFile.iloc[count, 1:]
        y_out = outputFile.iloc[count, 1:]

        inputArr.append(x_in)
        outputArr.append(y_out)
        count += 1
    return inputArr, outputArr


def dnnLearning(feature, target):
    pass


if __name__ == '__main__':

    x, y = extractCSV(inputFilePath, outputFilePath)
