import pandas as pd
import numpy as np

def get_representative_training_data(dataframe, y,value, pct, test_size):
    
    train_value_number = round((1 - test_size) * len(dataframe) * pct)
    train_notvalue_number = round((1-test_size) * len(dataframe) - train_value_number)
    filtered_value = dataframe[dataframe[y] == value].iloc[:train_value_number][y]
    index_value = dataframe[dataframe[y] == value].iloc[:train_value_number][y].index.tolist()
    filtered_not_value = dataframe[dataframe[y] != value].iloc[:train_notvalue_number][y]
    index_not_value = dataframe[dataframe[y] != value].iloc[:train_notvalue_number][y].index.tolist()
    index_value.extend(index_not_value)
    y_train = pd.concat([filtered_value, filtered_not_value])
    y_df = dataframe[y]
    y_test = y_df.drop(y_df.index[index_value])
    x_df = dataframe.drop(columns= [y])
    x_train  = np.array(x_df.iloc[index_value])
    x_test = np.array(x_df.drop(x_df.index[index_value]))

    return x_train, x_test, y_train, y_test


def split_into_representative_training_data(dataframe, x, y, value, pct, test_size):

    train_value_number = round((1 - test_size) * len(dataframe) * pct)
    train_notvalue_number = round((1-test_size) * len(dataframe) - train_value_number)
    filtered_value = y[y == value][:train_value_number]
    index_value = filtered_value.index.tolist()
    filtered_not_value = y[y != value][:train_notvalue_number]
    index_not_value = filtered_not_value.index.tolist()
    index_value.extend(index_not_value)
    y_train = pd.concat([filtered_value, filtered_not_value])
    y_test = y.drop(y.index[index_value])
    x_train = np.array(x.iloc[index_value])
    x_test = np.array(x.drop(x.index[index_value]))

    return x_train, x_test, y_train, y_test








