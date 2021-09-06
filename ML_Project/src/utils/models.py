import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, LSTM
from tensorflow.keras.optimizers import RMSprop
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, LSTM, MaxPooling1D, Conv1D, Flatten
from tensorflow.keras.callbacks import Callback
from sklearn.metrics import mean_squared_error, mean_absolute_error



def LSTM_preprocessing(data, step, train_size):
    """This function returns the values preprocessed to train a LSTM model
    parameters:
    data: dataframe 
    step: step size for the sliding window
    train_size = percentage of the train size

    returns: x and y divided in train and test already preprocessed to use the in a LSTM model
    """
    copy_last = data[-1:]
    LSTM_df = data[-1:]
    for i in range(step-1):
        LSTM_df = pd.concat([LSTM_df, copy_last])
    LSTM_df = pd.concat([data, LSTM_df])
    x_list = []
    y_list = []
    separator = int(train_size * len(data))
    for i in range(len(data)):
        D = i + step
        x_list.append([LSTM_df[x][i:D] for x in data.columns[2:]])
        y_list.append(LSTM_df['Close Price'][D:D+1])
    
    array_x = np.array(x_list)
    array_y = np.array(y_list)

    x_train, x_test = array_x[:separator], array_x[separator:]
    y_train, y_test = array_y[:separator], array_y[separator:]

    return x_train, x_test, y_train, y_test

def test_preprocessing(data, step, train_size):
    """This function returns the values preprocessed to train a LSTM model
    parameters:
    data: dataframe 
    step: step size for the sliding window
    train_size = percentage of the train size

    returns: x and y divided in train and test already preprocessed to use the in a LSTM model
    """
    rep_step = data.iloc[-step:, 2:]
    LSTM_df = pd.concat([data, rep_step])
    x_list = []
    y_list = []
    separator = int(train_size * len(data))
    for i in range(len(data)):
        D = i + step
        x_list.append([LSTM_df[x][i:D] for x in data.columns[2:]])
        y_list.append(LSTM_df['Close Price'][D:D+1])

    
    

def build_simple_rnn(num_units=128, embedding= 60, num_dense=32,lr=0.001):
    """
    Builds and compiles a simple RNN model
    Arguments:
            num_units: Number of units of a the simple RNN layer
            embedding: Embedding length
            num_dense: Number of neurons in the dense layer followed by the RNN layer
            lr: Learning rate (uses RMSprop optimizer)
    Returns:
            A compiled Keras model.
    """
    model = Sequential()
    # Long short term memory
    model.add(LSTM(units=num_units, input_shape=(9,embedding), activation="relu"))
    model.add(Dense(num_dense, activation="relu"))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer=RMSprop(learning_rate=lr),metrics=['mse'])
    
    return model


def ad_test(dataset):
    dftest = adfuller(dataset, autolag= 'AIC')
    print('1. ADF:', dftest[0])
    print('2. P-value:', dftest[1])
    print('3. Num of Lags:', dftest[2])
    print('4. Num of Observations used for ADF Regression and Critical Values Calculation:', dftest[3])
    print('5. Critical Values:')
    for key, val in dftest[4].items():
        print('\t', key, ': ', val)

def Time_Series_train_test_split(x, y, validation_size):
    """ splits x and y into train and test, keeping the time series""" 

    train_size = int(len(x) * (1 - validation_size))
    x_train, x_test = x[0:train_size], x[train_size:]
    y_train, y_test = y[0: train_size], y[train_size:] 

    return x_train, x_test, y_train, y_test

def build_CNN_model(filters = 64, optimizer = 'adam', embedding = 60 ):
    model = Sequential()
    model.add(Conv1D(filters= filters, kernel_size = 2, activation = 'relu', input_shape= (9, embedding)))
    model.add(MaxPooling1D(pool_size= 2))
    model.add(Flatten())
    model.add(Dense(50, activation = 'relu'))
    model.add(Dense(1))
    model.compile(optimizer = 'adam', loss= 'mse')

    return model

def try_embedding(df, embedding_list):
    for i in embedding_list:
        x_train, x_test, y_train, y_test = LSTM_preprocessing(df, step= i, train_size= 0.5)
        model = build_CNN_model(embedding= i)
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        print('embedding:', i)
        print('error:', mean_squared_error(y_pred, y_test))
        print('##########################################')
    return

def try_epochs(df, epoch_list):
    for i in epoch_list:
        x_train, x_test, y_train, y_test = LSTM_preprocessing(df, step= 5, train_size= 0.5)
        model = build_CNN_model(embedding= 5)
        model.fit(x_train, y_train, epochs= i)
        y_pred = model.predict(x_test)
        print('embedding:', i)
        print('error:', mean_squared_error(y_pred, y_test))
        print('##########################################')

def try_batch(df, batch_size):
    for i in batch_size:
        x_train, x_test, y_train, y_test = LSTM_preprocessing(df, step= 5, train_size= 0.5)
        model = build_CNN_model(embedding= 5)
        model.fit(x_train, y_train, batch_size= i)
        y_pred = model.predict(x_test)
        print('embedding:', i)
        print('error:', mean_squared_error(y_pred, y_test))
        print('##########################################')