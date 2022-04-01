import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

inputFilePath = '../dataset/input.csv'
outputFilePath = '../dataset/output.csv'
modelFilePath = '../dataset/trainedCNNModel.h5'

inputDataSize, numOfClasses = 81, 10
lengthData = 100000


def extractCSV(inputPath, outputPath, lenData):
    global inputDataSize
    inputArr, outputArr = np.zeros((lenData, 9, 9, 1)), np.zeros((lenData, inputDataSize))
    inputFile = pd.read_csv(inputPath)
    outputFile = pd.read_csv(outputPath)

    count = 0
    while count < lenData:
        x_in = np.array(inputFile.iloc[count, 1:]).reshape((9, 9, 1))
        y_out = np.array(outputFile.iloc[count, 1:])
        inputArr[count, :] = x_in
        outputArr[count, :] = y_out
        count += 1
    return inputArr, outputArr


def dnnArchitecture(inputSize, numClasses):

    inputSize_ = inputSize

    model = keras.Sequential()

    model.add(layers.Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(9, 9, 1)))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(128, kernel_size=(1, 1), activation='relu', padding='same'))
    model.add(layers.Flatten())

    model.add(layers.Dense(81 * 9))
    model.add(layers.Reshape((-1, 9)))
    model.add(layers.Activation('softmax'))

    return model


def trainModel(modelPath, trainData, testTarget, inputSize, numClasses):

    model = dnnArchitecture(inputSize, numClasses)
    adam = keras.optimizers.Adam(lr=0.001)

    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)
    model.summary()
    callbacks = [
        keras.callbacks.ModelCheckpoint(modelPath, save_best_only=True)
    ]
    epochs = 10
    history = model.fit(
        trainData, testTarget, validation_split=0.2,
        batch_size=32, epochs=epochs, callbacks=callbacks
    )

    # list all data in history
    print(history.history.keys())

    # summarize history for accuracy
    # fig1 = plt.figure(figsize=(8, 6))
    # plt.title("Training history - Accuracy", fontsize=20)
    # plt.plot(history.history['acc'])
    # plt.plot(history.history['val_acc'])
    # plt.ylabel('accuracy')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    # plt.savefig(f'../dataset/val_acc_plot.png', )

    # summarize history for loss
    fig2 = plt.figure(figsize=(8, 6))
    plt.title("Training history - Loss", fontsize=20)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper right')
    plt.savefig(f'../dataset/val_loss_plot.png', )
    plt.show()


def main(args):
    keras.backend.clear_session()
    os.environ['DML_VISIBLE_DEVICES'] = '0'

    trainSet, targetSet = extractCSV(inputFilePath, outputFilePath, lengthData)
    # trainSet = keras.utils.to_categorical(trainSet, numOfClasses)
    # targetSet = keras.utils.to_categorical(targetSet, numOfClasses)

    trainModel(modelFilePath, trainSet, targetSet, inputDataSize, numOfClasses)


if __name__ == '__main__':
    main(sys.argv)

