
import Sudoku
import numpy as np
import pygame

board = Sudoku.exportSeries().reshape((9, 9, 1))
print(board.shape)


from scripts import inferenceSudoku
import tensorflow as tf

model = tf.keras.models.load_model('dataset/trainedCNNModel.h5')
prediction = inferenceSudoku.inference_sudoku(model, board, 1)
print(prediction)
