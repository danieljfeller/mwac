import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import pandas as pd

#############
# load data #
#############

historical_data = pd.read_csv("data/cleaned_hermit_lake_snowdepth.csv")
historical_averages = pd.read_csv("data/historical_averages.csv")
historical_averages['historical_depth'] = historical_averages['depth_cm']
historical_averages = historical_averages.drop(['depth_cm'], axis = 1)

###############
# define tabs #
###############


tab1, tab2 = st.tabs(["Weather Data Viewer", "Snowpack Data Viewer"])

with tab1:

    # create synthetic data
    df = pd.DataFrame({
        'day': np.arange(1, 101),
        'max_temp': np.random.randint(20, 33, size=100),
        'new_snow_cm': np.random.randint(1, 11, size=100),
        'avg_wind': np.random.uniform(1, 100, size=100),
        'mean_direction': np.random.uniform(180, 270, size=100)
    })

    df['max_wind'] = df['avg_wind'] + np.random.uniform(3, 12, size=100)
    df['min_wind'] = df['avg_wind'] - np.random.uniform(5, 12, size=100)
    df['min_temp'] = df['max_temp'] - np.random.uniform(4, 20, size=100)
    df['new_swe'] = df['new_snow_cm'] * np.random.uniform(0.1, 0.15, size=100)

    # temperature
    st.divider()
    st.title("Temperature - 5000 ft.")
    st.line_chart(df[['day', 'max_temp', 'min_temp']], x = 'day', y = ['max_temp', 'min_temp'])

    # wind lind chart; daily max, min, and avg

    st.divider()
    st.title("Daily Wind Speeds")
    st.area_chart(df[['day', 'max_wind', 'avg_wind', 'min_wind']], x = 'day')

    # precipitation; density, new snow (cm),
    st.divider()
    st.title("Precipitation")
    st.bar_chart(df[['day', 'new_snow_cm', 'new_swe']], x = 'day')

with tab2:
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
              "175m", "-2%")
    col2.metric("Total Snowfall", "350cm", "+5%")

    # SELECT BOX
    st.divider()
    winter_selection = st.selectbox("Select Year", options = set(historical_data.winter), index = 4)
    selection = historical_data.loc[historical_data.winter==winter_selection, ['day_of_winter', 'depth_cm']]
    df = selection.merge(historical_averages, on = 'day_of_winter', how = 'right')


    # LINE CHART
    st.area_chart(df, x="day_of_winter", y=["historical_depth", "depth_cm"])






