from flask import Flask, flash, request, render_template, redirect, url_for
from posixpath import sep
import flask
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import os
import json
import sys
from tensorflow import keras
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


dir = os.path.dirname
path = dir(dir(dir(__file__)))
sys.path.append(path)

from src.utils.apis_tb import read_json
from src.utils.models import LSTM_preprocessing
from src.utils.mining_data_tb import put_features
from src.utils import sql_tb as sql

print(sys.path)
model_path = 'C:\\Users\\jarai\\Desktop\\Python_work\\TheBridge\\Alumno\\Javier_Araiz_TheBridge\\ML_Project\\src\\models\\tuned_CNN.h5'
Final_model = keras.models.load_model(model_path)


df = None
menu = st.sidebar.selectbox('Menu:',
            options=["Welcome", "Prediction graphs", "API", 'Prediction', 'model comparison'])


if menu == 'Welcome':
    st.title("ML models for EURUSD price prediction")
    st.write('Through this proyect we have tried different Machine Learning models with the purpose of trying to predict FOREX. For thet matter we have used the Close price as independent variable and high bid, low bid alog with the standard and exponential averages as dependent variables ')
if menu == 'Prediction graphs':
    st.caching.clear_cache()
    st.title('Prediction graphs')
    graph = st.selectbox('Select a model:',
                        options= ['LSTM', 'Linear Regression','ARIMA', 'CNN', 'tuned CNN'])
    if graph == 'LSTM':
        print(path + os.sep + 'Resources' + os.sep + 'Images' + os.sep + 'LSTM_model.png')
        image = Image.open(path + os.sep + 'Resources' + os.sep + 'Images' + os.sep + 'LSTM_model.png')
        st.image(image,use_column_width=True)
        st.write('Despite there´s a difference of 0,01 between the prices, we can appreciate that the neural network guesses correctly the trends. Embedding is set on 60 periods of one minute and forecast is for the next period.')
    if graph == 'Linear Regression':
        image = Image.open(path + os.sep + 'Resources' + os.sep + 'Images' + os.sep + 'Linear_Regression_model.png')
        st.image(image,use_column_width=True)
        st.write('Here we can observe the Linear Regression model is very accurate compared to the actual prices. However, the problem is that Scikit learn does not support 3d matrixes so there´s no form to be used as a method of timeseries forecasting.')

    if graph == 'ARIMA':
        image = Image,open(path + os.sep + 'Resources' + os.sep + 'Images' + os.sep + 'Arima_model.png')
    if graph == 'CNN':
        image = Image.open(path + os.sep + 'Resources' + os.sep + 'Images' + os.sep + 'CNN_model.png')
        st.image(image)
    if graph == 'tuned CNN':
        image = Image.open(path + os.sep + 'Resources' + os.sep + 'Images' + os.sep + 'tuned_CNN_model.png')
    
if menu == 'API':
    
    st.table(pd.read_json('http://localhost:6060/get_API?Token_id=L16092222'))

if menu == 'Prediction':
    
    st.write('drag a csv file so that the model can make a prediction. file must have these columns: Date,Time,Bar OPEN Bid Quote,Bar HIGH Bid Quote,Bar LOW Bid Quote,Bar CLOSE Bid Quote,Volume')
    csv = st.file_uploader('upload csv')
    if csv is not None:
        columns = ['Date', 'Time','Bar OPEN Bid Quote','Bar HIGH Bid Quote','Bar LOW Bid Quote','Bar CLOSE Bid Quote','Volume']
        print(sys.path)
        file = pd.read_csv(csv)
        file.columns = columns
        file = put_features(file)
        file['Close Price'] = file['Bar CLOSE Bid Quote']
        file = file.drop(columns='Bar CLOSE Bid Quote', axis= 1)
        file = file.set_index(file['Date'])
        x_train, x_test, y_train, y_test = LSTM_preprocessing(file, step= 10, train_size= 0.8)
        prediction = Final_model.predict(x_test)
        
        # Plot the prediction

        
        
        chart = plt.figure()
        plt.plot(prediction, c = 'red', label= 'Prediction')
        plt.plot(y_test, c= 'blue', label= 'actual price')
        plt.xlabel('table row nº')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

        st.pyplot(chart)
        
if menu == 'model comparison':
    sql_json_readed = read_json(path + os.sep + 'src' + os.sep + 'manage_sql.json')
    IP_DNS = sql_json_readed["IP_DNS"]
    USER = sql_json_readed["USER"]
    PASSWORD = sql_json_readed["PASSWORD"]
    BD_NAME = sql_json_readed["BD_NAME"]
    PORT = sql_json_readed["PORT"]
    mysql_db = sql.MySQL(IP_DNS=IP_DNS, USER=USER, PASSWORD=PASSWORD, BD_NAME=BD_NAME, PORT=PORT)
    mysql_db.connect()
    db_connection_str = mysql_db.SQL_ALCHEMY
    db_connection = create_engine(db_connection_str)
    comparison = pd.read_sql('SELECT * FROM model_comparison', con=db_connection)
    st.table(comparison)