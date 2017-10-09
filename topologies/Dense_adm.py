""" Denoising Auto-Encoder """

from keras.models import Sequential
from keras.layers.convolutional import Conv1D
from keras.layers import Dense, Activation, Reshape, Flatten
from keras.layers import LSTM
from keras import optimizers



def build_model(input_shape):
    seq_length = input_shape[0]

    # build it!
    model = Sequential()

    model.add(Dense(128,input_shape=input_shape))
    #model.add(Activation('sigmoid'))
    # dense
    model.add(Dense(units=seq_length))
    model.add(Activation('relu'))

    #model.add(Dense(units=128))
    #model.add(Activation('relu'))

    model.add(Dense(units=60))
    model.add(Activation('relu'))

    model.add(Dense(units=60))
    model.add(Activation('relu'))

    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    # compile it!
    model.compile(loss='mean_squared_error',
                  optimizer='adam',
                  metrics=['acc', 'mae', 'mse'])

    return model
