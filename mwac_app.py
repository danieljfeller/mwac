import streamlit as st
import pandas as pd




## load & format data
historical_data = pd.read_csv("data/cleaned_hermit_lake_snowdepth.csv")
historical_averages = pd.read_csv("data/historical_averages.csv")
historical_averages['historical_depth'] = historical_averages['depth_cm']
historical_averages = historical_averages.drop(['depth_cm'], axis = 1)

# TITLE & INFORMATION
st.title("Snowdepth at Hermit Lake")
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(historical_data)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='hermit_lake_snowdepth.csv',
    mime='text/csv',
)
st.divider()

# METRICS
today = historical_data.loc[historical_data.winter == '2023-2024',]['day_of_winter'].max()

col1, col2 = st.columns(2)
col1.metric("Current Snowpack",
          "55cm", "-67%")
col2.metric("Total Snowfall", "251cm", "-43%")

# SELECT BOX
st.divider()
winter_selection = st.selectbox("Select Year", options = set(historical_data.winter), index = 4)
selection = historical_data.loc[historical_data.winter==winter_selection, ['day_of_winter', 'depth_cm']]
df = selection.merge(historical_averages, on = 'day_of_winter', how = 'right')


# LINE CHART
st.area_chart(df, x="day_of_winter", y=["historical_depth", "depth_cm"])



