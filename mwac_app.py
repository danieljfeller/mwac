import streamlit as st
import pandas as pd

st.title('Historical Average Snow Depth - Mt. Washington')

## load data
historical_data = pd.read_csv("data/cleaned_hermit_lake_snowdepth.csv")
historical_averages = pd.read_csv("data/historical_averages.csv")

# change variable name
historical_averages['historical_depth'] = historical_averages['depth_cm']
historical_averages = historical_averages.drop(['depth_cm'], axis = 1)

# isolate winter of interest
winter_selection = st.selectbox("Select Year", options = set(historical_data.winter))
selection = historical_data.loc[historical_data.winter==winter_selection, ['day_of_winter', 'depth_cm']]
df = selection.merge(historical_averages, on = 'day_of_winter', how = 'right')

st.line_chart(df, x="day_of_winter", y=["historical_depth", "depth_cm"])

