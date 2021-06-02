
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


dir = os.path.dirname
path = dir(dir(dir(__file__)))
sys.path.append(path)

from src.utils.apis_tb import read_json


df = None
menu = st.sidebar.selectbox('Menu:',
            options=["Welcome", "Graphs", "API"])


if menu == 'Welcome':
    st.title("The impact of oil price in shipping business")
    st.write('The purpose of this web app is to show different regarding the maritime industry and oil price in order to see if there´s a possible relation between them. The source from this datasets is UNCTAD database.')
if menu == 'Graphs':
    st.caching.clear_cache()
    st.title('Graphs')
    graph = st.selectbox('Select a graph:',
                        options= ['BrentvsBDI', 'fleet growth','fleet growth by ship type', 'fleet and seatrade correlation', 'seatrade GDP correlation', 'seatrade and Brent price correlation'])
    if graph == 'BrentvsBDI':
        print(path + os.sep + 'Resources' + os.sep + 'BrentvsBDI.png')
        image = Image.open(path + os.sep + 'Resources' + os.sep + 'BrentvsBDI.png')
        st.image(image,use_column_width=True)
        st.write('Here we can see both indices take a very similar trend during the hole period')
    if graph == 'fleet growth':
        col1, col2 = st.beta_columns([2, 4])
        with col1:
            image = Image.open(path + os.sep + 'Resources' + os.sep + 'Total_fleet_deadweight_evol.png')
            st.image(image,use_column_width=True)
        with col2:
            image2= Image.open(path + os.sep +  'Resources' + os.sep + 'Number_of_ships.png')
            st.image (image2,use_column_width=True)
        st.write('Here there´s a comparison of fleet growth on a Deadweight basis (left) and number of ships (right)')
    if graph == 'fleet growth by ship type':
        image = Image,open(path + os.sep + 'Resources' + os.sep + 'World_fleet_evol.png')
    if graph == 'fleet and seatrade correlation':
        image = Image.open(path + os.sep + 'Resources' + os.sep + 'fleet_seatrade.png')
        st.image(image)
    if graph == 'seatrade GDP correlation':
        image = Image.open(path + os.sep + 'Resources' + os.sep + 'seatrade_world_GDP.png')
        st.image(image)
    if graph == 'seatrade and Brent price correlation':
        image = Image.open(path + os.sep + 'Resources' + os.sep + 'seatrade_Brent.png')
if menu == 'API':
    #user_input = st.text_area("Enter password")
    #if st.button('Submmit'):
        #answer = 'http:localhost:6060/get_API' + '?password=' + user_input
        #readed_json = pd.read_csv(answer)
    st.table(pd.read_json('http://localhost:6060/get_API?Token_id=L16092222'))
    


    



