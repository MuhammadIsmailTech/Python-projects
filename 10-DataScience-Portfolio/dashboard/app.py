import sys
import os
import streamlit as st
import pandas as pd, joblib
from src.data_cleaning import load_data, clean_data
from src.feature_engineering import add_features



# Add project root to Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.data_cleaning import load_data, clean_data


st.title('Data Science Portfolio - Housing Dashboard')
df = load_data()
df = clean_data(df)
df = add_features(df)
st.write(df.head())

loc = st.selectbox('Location', df['Location'].unique())
filtered = df[df['Location']==loc]
st.write(filtered)

st.subheader('Predict price')
rooms = st.number_input('Rooms', 1, 10, 3)
area = st.number_input('Area', 100, 10000, 1000)
loc_map = {'Rural':0,'Suburban':1,'Urban':2}
loc_choice = st.selectbox('Location for prediction', list(loc_map.keys()))
model = None
try:
    model = joblib.load('model/trained_model.pkl')
except Exception as e:
    st.warning('Model not found. Run src/train_model.py')
if model:
    X = pd.DataFrame([[rooms,area,loc_map[loc_choice]]], columns=['Rooms','Area','Location_code'])
    pred = model.predict(X)[0]
    st.write(f'Estimated price: ${pred:,.2f}')
