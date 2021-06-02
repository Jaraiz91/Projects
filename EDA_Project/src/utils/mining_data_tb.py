# función para normalizar los csv que no separa bien las columnas
from numpy import NaN
import pandas as pd


def normalize_dataframe(dataframe, sep):
    dataframe = dataframe[0].str.split(sep, expand= True)
    dataframe.columns = dataframe.iloc[0,:]
    dataframe = dataframe.drop(dataframe.index[0])
    return dataframe

# función para contar los valores de una columna que son números, los convierte en enteros y el resto de valores los devuelve NaN
def count_numbers_in_column(dataframe, column):
    n = 0
    nserie = []
    for val in dataframe[column]:
        try:
            if val.isnumeric() == True:
                nserie.append(int(val))
                n +=1
            else:
                val = NaN
                nserie.append(val)
        except:
            nserie.append(val)
    dataframe[column] = nserie
    print('Numbers in columns:', n)
    return dataframe

# función para quitar las comillas de los valores dentro de una serie
def drop_quot_marks(dataframe, columna):
    serie = []
    for val in dataframe[columna]:
        new_val = []
        for x in val:
            if x != '"':
                new_val.append(x)
        val = ''.join(new_val)
        serie.append(val)
    dataframe[columna] = serie
    return dataframe
    
# función para convertir un dataframe en entero

def convert_df_toint(dataframe):
    for col in dataframe:
        dataframe[col] = dataframe[col].apply(pd.to_numeric)
        
    return dataframe

# función para pasar el timeseries a años

def year_timeseries(dataframe):
    serie = []
    for val in dataframe.index:
        val = val.year
        serie.append(val)
    dataframe.index = serie
    return dataframe