""" Denoising Auto-Encoder """

from keras.models import Sequential
from keras.layers.convolutional import Conv1D
from keras.layers import Dense, Activation, Reshape, Flatten
from keras.layers import LSTM
from keras import optimizers



def build_model(input_shape):

    model = Sequential()
    model.add(LSTM(128, input_shape=input_shape, return_sequences=True,
		kernel_initializer='random_uniform'))
    model.add(Dense(32))
    model.add(Activation('relu'))
    model.add(Dense(1))
    model.add(Activation('relu'))
    model.compile(loss='mean_squared_error',optimizer='adam',metrics=['acc', 'mae', 'mse'])
    return model
