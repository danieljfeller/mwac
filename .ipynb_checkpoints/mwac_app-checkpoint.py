import streamlit as st
import pandas as pd

st.title('Historical Average Snow Depth - Mt. Washington')



historical_data = pd.read_csv("data/cleaned_hermit_lake_snowdepth.csv")
historical_averages = pd.read_csv("data/historical_averages.csv")


st.subheader('Raw data')
st.write(historical_averages)


st.line_chart(historical_averages, x="date", y="depth_cm")
