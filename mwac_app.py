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

################
# prepare data #
################

df = pd.DataFrame({
    'day': np.arange(1, 15),
    'max_temp': np.random.randint(20, 33, size=14),
    'new_snow_cm': np.random.randint(1, 11, size=14),
    'avg_wind': np.random.uniform(1, 100, size=14),
    'mean_direction': np.random.uniform(180, 270, size=14)
})

df['max_wind'] = df['avg_wind'] + np.random.uniform(3, 12, size=14)
df['min_wind'] = df['avg_wind'] - np.random.uniform(5, 12, size=14)
df['min_temp'] = df['max_temp'] - np.random.uniform(4, 20, size=14)
df['new_swe_mm'] = df['new_snow_cm'] * np.random.normal(0.1, 0.15, size=14)

df['snow_density_pct'] = (df['new_swe_mm'] / df['new_snow_cm']) * 100

###############
# define tabs #
###############


tab1, tab2, tab3, tab4 = st.tabs(['Snowpack Tracker', 'Recent Weather', 'Forecast', 'Download Our Data'])

###################
# Skier / Climber #
###################

with tab1:
    st.image('media/mwac_logo.png', use_container_width  = 'always')

    selected_location = st.selectbox(
    "Select Weather Station:",
    ("Hermit Lake", "Harvard Cabin", "Grey Knob", "Mount Washington Summit", "The Lip", "Pinkham Notch"),
    index=None,
    placeholder="Choose a location...")
    st.write("You selected:", selected_location)

    # 24 hr metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("24h snowfall (cm)", "5cm")
    col2.metric("48h snowfall", "10cm")
    col3.metric("72h snowfall", "12cm")
    col4.metric("7d snowfall", "43cm")
    col5.metric("Season snowfall", "210cm")

    st.header('Historical Comparison', divider='rainbow')


    # METRICS
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    csv = convert_df(historical_data)
    today = historical_data.loc[historical_data.winter == '2023-2024',]['day_of_winter'].max()

    col1, col2 = st.columns(2)
    col1.metric("Current Snowpack",
              "111cm", "-8% YoY")
    col2.metric("Total Snowfall", "350cm", "+5% YoY")

    # SELECT BOX
    winter_selection3 = st.selectbox("Select YWinter",
                                    options = set(historical_data.winter),
                                    placeholder="2023-2024")
    selection = historical_data.loc[historical_data.winter==winter_selection3, ['day_of_winter', 'depth_cm']]
    df = selection.merge(historical_averages, on = 'day_of_winter', how = 'right')


    # LINE CHART
    st.area_chart(df, x="day_of_winter", y=["historical_depth", "depth_cm"])

with tab2:

    #################
    # Generate Data #
    #################

    st.image('media/mwac_logo.png', use_container_width  = 'always')


    selected_location = st.selectbox(
    "Weather Station:",
    ("Hermit Lake", "Harvard Cabin", "Grey Knob", "Mount Washington Summit", "The Lip", "Pinkham Notch"),
    index=None,
    placeholder="Choose a location...")


    selected_timeframe = st.selectbox(
    "Timeframe",
    ("Past 24 hours", "Past 48 hours", "Past 72 hours", "Past 7 days", "Past 30 days"),
    index=None,
    placeholder="Choose a timeframe...")

    
    # 24 hr metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Average Wind",
              "20mph", "+10mph")
    col2.metric("Max Wind", "43mph")
    col3.metric("24 snowfall (cm)", "5cm", "+5cm")
    col4.metric("Max Temp", "34F")
    col5.metric("Min Temp", "10F")

    st.header('Past weather summary', divider='rainbow')
    st.markdown('''Over the past 7 days, temperatures have fluctuated across the Presidential Range. Significant recent snowfall and high and variable winds have yielded a complex snowpack.''')



################
# Professional #
################

with tab3:    

    st.image('media/mwac_logo.png', use_container_width  = 'always')
 
    # METRICS
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    csv = convert_df(historical_data)
    today = historical_data.loc[historical_data.winter == '2023-2024',]['day_of_winter'].max()

    col1, col2 = st.columns(2)
    col1.metric("Current Snowpack",
              "111cm", "-8% YoY")
    col2.metric("Total Snowfall", "350cm", "+5% YoY")

    # SELECT BOX
    winter2_selection = st.selectbox("Select Year",
                                    options = set(historical_data.winter),
                                    placeholder="2023-2024")
    selection = historical_data.loc[historical_data.winter==winter2_selection, ['day_of_winter', 'depth_cm']]
    df = selection.merge(historical_averages, on = 'day_of_winter', how = 'right')
    df['day'] = df['day_of_winter'] 
    df['new_snow_cm'] = 1
    df['snow_density_pct'] = 0.20
    df['max_temp'] = 32
    df['min_temp'] = 20
    df['max_wind'] = 15
    df['min_wind'] = 5
    df['avg_wind'] = 10

    # LINE CHART
    st.area_chart(df, x="day_of_winter", y=["historical_depth", "depth_cm"])
    
    st.header('New Snow & Snow Density', divider='rainbow')
    print(df.columns)
    st.bar_chart(df[['day', 'new_snow_cm', 'snow_density_pct']], x = 'day') # for new_snow
    #st.line_chart # density

    st.divider()
    st.header('Wind Speed', divider='rainbow')
    st.area_chart(df[['day', 'max_wind', 'avg_wind', 'min_wind']], x = 'day')
    # add axis labels for day


    st.divider()
    st.header('Temperature', divider='rainbow')
    #st.line_chart(df[['day', 'max_temp', 'min_temp']], x = 'day', y = ['max_temp', 'min_temp'])
    # add axis labels for day



##############
# Researcher #
##############

with tab4:

    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(historical_data)

    st.image('media/mwac_logo.png', use_container_width  = 'always')
    st.image('media/snowplot.png', use_container_width  = 'always')

    st.markdown('''
Snowpack observations have been systematically collected since 2001 at the Hermit Lake Ranger Station, located just below Tuckerman Ravine on Mount Washington, New Hampshire. These records are accessible for download in CSV file format.''')

    st.header('Download the data', divider='rainbow')
    st.markdown('''Data is available for research use only. No commercial usage of the data is permitted without explicit permission of the Mount Washington Avalanche Center''')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='hermit_lake_snowdepth.csv',
        mime='text/csv',
    )







