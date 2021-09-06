import pandas as pd
import numpy as np
import os, sys



def merge_csv(base_name, range_number, column_name, file_name, path, start_number= 0):

    """" The function saves a csv file with all the csv files you want to join
    arguments:
    base_name: base name that share all the files in order to make the loop inside the function
    start_number: this number is used in case the file number must start from a number other than one. Default value is 0
    range_number: list or tuple with the start and end numbers to the loop
    column_name: list with the names of the columns
    file_name : desired name for the new file you want to save
    path: path to folder where the new_file must be stored
    
    Returns:
    a new merged csv file
    
    """
    

            

    for i in range(range_number[0], range_number[1]):
        if i == 1:
            data = pd.read_csv(base_name + str(start_number + i) + '.csv', header= None)
            df = pd.DataFrame(data)
            df.columns = column_name
            data1 = pd.read_csv(base_name + str(start_number + i + 1) + '.csv', header = None)
            df1 = pd.DataFrame(data1)
            df1.columns = column_name
            merged_df = pd.concat([df, df1])
            
        else:
            data = pd.read_csv(base_name + str(start_number + i + 1) + '.csv', header= None)
            df = pd.DataFrame(data)
            df.columns = column_name
            df1 = merged_df
            merged_df = pd.concat([df1, data])

    path_to_file = path + os.sep + file_name + '.csv'
    merged_df.to_csv(path_to_file, header= True, index= False)

    return

def save_merged_csv(csv1, csv2, file_name, path): 

    """This function concatenates 2 csv that already have same column names and
    saves the new file in the given path as parameter"""

    data1 = pd.read_csv(csv1)
    df1 = pd.DataFrame(data1)

    data2 = pd.read_csv(csv2)
    df2 = pd.DataFrame(data2)

    concat_df = pd.concat([df1, df2])
    path_to_file = path + os.sep + file_name + '.csv'
    concat_df.to_csv(path_to_file, header= True, index= False)

    return

def add_features(df, file_name, path):

    """ This function add the features needed for trading time series
    arguments:
    df : Dataframe to be used for adding the features

    returns:
    A saved file of csv modified with the new features

    """
    df['SMA_5'] = df['Bar CLOSE Bid Quote'].rolling(window=5).mean()
    df['SMA_20'] = df['Bar CLOSE Bid Quote'].rolling(window=20).mean()
    df['SMA_200'] = df['Bar CLOSE Bid Quote'].rolling(window=200).mean()
    df['EMA_20'] = df['Bar CLOSE Bid Quote'].ewm(span=20, min_periods=20, adjust=True).mean()

    path_to_file = path + os.sep + file_name + '.csv'

    df.to_csv(path_to_file, header= True, index= False)

    return

def put_features(df):

    df['SMA_5'] = df['Bar CLOSE Bid Quote'].rolling(window=5).mean()
    df['SMA_20'] = df['Bar CLOSE Bid Quote'].rolling(window=20).mean()
    df['SMA_200'] = df['Bar CLOSE Bid Quote'].rolling(window=200).mean()
    df['EMA_20'] = df['Bar CLOSE Bid Quote'].ewm(span=20, min_periods=20, adjust=True).mean()

    return df

def parser(x):
    """ function to parse object into datetime when reading a csv file"""
    return datetime.strptime(x, '%Y.%m.%d')

def x_dict_y_dict(data, step):
    """ Function designed to check if LSTM_preprocessing is doing changes in data as desired"""
    copy_last = data[-1:]
    LSTM_df = data[-1:]
    for i in range(step-1):
        LSTM_df = pd.concat([LSTM_df, copy_last])
    LSTM_df = pd.concat([data, LSTM_df])
    x_list = []
    y_list = []
    for i in range(len(data)):
        D = i + step
        x_list.append([LSTM_df[x][i:D] for x in data.columns[:]])
        y_list.append({'date': LSTM_df['Date'][D:D+1], 'time': LSTM_df['Time'][D:D+1], 'close price': LSTM_df['Close Price'][D:D+1]})
    return x_list, y_list