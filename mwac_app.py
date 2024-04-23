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


tab1, tab2, tab3 = st.tabs(['Avalanche Weather Summary', 'Snow & Weather Data', 'Download'])

###################
# Skier / Climber #
###################

with tab1:

    #################
    # Generate Data #
    #################

    # 24 hr metrics
    st.header('Past 48hour Weather Stats', divider='rainbow')
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Average Wind",
              "20mph", "+10mph")
    col2.metric("Max Wind", "43mph")
    col3.metric("24 snowfall (cm)", "5cm", "+5cm")
    col4.metric("Max Temp", "34F")
    col5.metric("Min Temp", "10F")

    st.header('AI-generated past weather summary', divider='rainbow')
    st.markdown('''Over the past 7 days, temperatures have fluctuated across the Presidential Range. Significant recent snowfall and high and variable winds have yielded a complex snowpack.''')

    st.header('AI-generated 48hr forecast summary', divider='rainbow')
    st.markdown('''The next two days will include sporadic snow showers  entail significant wind speeds, with temperatures ranging from -10°F to 35°F. The forecast predicts accumulative snowfall reaching up to 9 inches over the period, accompanied by rapid changes in weather conditions, including sunny days and snow showers. This variability underscores the mountain's reputation for unpredictable and extreme weather conditions, exemplifying the challenges of meteorological forecasting in alpine environments. ''')



################
# Professional #
################

with tab2:
    st.image('huntington.jpeg', use_column_width  = 'always')


    st.header('Forecast Data', divider='rainbow')

    st.subheader('New Snow & Snow Density')
    st.bar_chart(df[['day', 'new_snow_cm', 'snow_density_pct']], x = 'day') # for new_snow
    #st.line_chart # density

    st.subheader('Wind Speed')
    st.area_chart(df[['day', 'max_wind', 'avg_wind', 'min_wind']], x = 'day')


    st.divider()
    st.subheader('Temperature')
    st.line_chart(df[['day', 'max_temp', 'min_temp']], x = 'day', y = ['max_temp', 'min_temp'])
    # add axis labels for day


    # CHART 1: COMBINED BAR AND LINE CHART
    # precipitation; density, new snow (cm)
    # add axis labels for day
    st.divider()
    st.title('Past Weather Data')
    st.header('New Snow & Snow Density', divider='rainbow')
    st.bar_chart(df[['day', 'new_snow_cm', 'snow_density_pct']], x = 'day') # for new_snow
    #st.line_chart # density

    st.divider()
    st.header('Wind Speed', divider='rainbow')
    st.area_chart(df[['day', 'max_wind', 'avg_wind', 'min_wind']], x = 'day')
    # add axis labels for day


    st.divider()
    st.header('Temperature', divider='rainbow')
    st.line_chart(df[['day', 'max_temp', 'min_temp']], x = 'day', y = ['max_temp', 'min_temp'])
    # add axis labels for day

    # wind lind chart; daily max, min, and avg




##############
# Researcher #
##############

with tab3:

    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(historical_data)

    st.header('Hermit Lake Snowplot - Since 2001', divider='rainbow')
    st.image('mwac_logo.png', use_column_width  = 'always')
    st.image('snowplot.png', use_column_width  = 'always')

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


    # TITLE & INFORMATION
    st.header('Hermit Lake Snowdepth vs. Seasonal Averages', divider='rainbow')


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
    winter_selection = st.selectbox("Select Year",
                                    options = set(historical_data.winter),
                                    placeholder="2023-2024")
    selection = historical_data.loc[historical_data.winter==winter_selection, ['day_of_winter', 'depth_cm']]
    df = selection.merge(historical_averages, on = 'day_of_winter', how = 'right')


    # LINE CHART
    st.area_chart(df, x="day_of_winter", y=["historical_depth", "depth_cm"])




