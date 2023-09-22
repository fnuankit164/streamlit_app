import streamlit as st
import pandas as pd
import requests
import snowflake.connector as conn

st.title("My Parents New Healthy Diner")
st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗Kale, Spinach & Rocket Smoothie')
st.text('🐔Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avacado Toast')
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
st.dataframe(fruits_to_show)

st.header('Fruityvice Fruit Advice!')
fruit_choice = st.text_input('What fruit would you like information about?', 'kiwi')
st.write('The user entered', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
st.dataframe(fruityvice_normalized)

my_cxn = conn.connect(**st.secrets["snowflake"])
my_cur = my_cxn.cursor()
my_cur.execute("Select * from fruit_load_list")
my_data_row = my_cur.fetchall()
st.header("The fruit load list cointains:")
st.dataframe(my_data_row)
fruit_name = st.text_input('What fruit would you like to add?')
my_cur.execute('insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values (fruit_name)')
