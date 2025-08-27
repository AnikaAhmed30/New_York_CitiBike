import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime as dt
from numerize.numerize import numerize

########################### Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'CitiBikes Strategy Dashboard', layout='wide')
st.title("CitiBikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv("df_daily.csv")
top20= pd.read_csv("top20.csv")
sample_df= pd.read_csv("sample_data_V2.csv")

######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("""### This dashboard provides an interactive interface to explore and visualize data insights. It includes charts built with Plotly and a geospatial map created with kepler.gl. Use the visualizations below to analyze trends and patterns in the dataset.""")


### Create the dual axis line chart page ###
    
elif page == 'Weather and bike usage':
    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig_2.add_trace(
        go.Scatter(x=df['date'], y=df['bike_rides_daily'], name='Daily Bike Rides', marker={'color': 'blue'}),
        secondary_y=False)
    fig_2.add_trace(
        go.Scatter(x=df['date'], y=df['avgWeather'], name='Daily Weather', marker={'color': 'red'}),
        secondary_y=True)
    fig_2.update_layout(title='Daily Bike Rides and Weather in New York',
                        height=400)
    st.plotly_chart(fig_2, use_container_width=True)  # Ensure this is indented with 4 spaces
    st.markdown("""This chart shows daily bike trip trends. Peaks may indicate high demand days (e.g., weekends or warm weather), suggesting areas for supply adjustments.
    """)


### Most popular stations page

elif page == 'Most popular stations':
    

# Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=sample_df['season'].unique(),
    default=sample_df['season'].unique())

    df1 = sample_df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
    
# Bar chart

    st.header("Top 20 Most Popular Bike Stations in New York")

    fig = go.Figure(go.Bar(
    x=top20['start_station_name'],
    y=top20['value'],
    marker={'color': top20['value'], 'colorscale': 'Blues'}))
    fig.update_layout(
    title='Top 20 Most Popular Bike Stations in New York',
    xaxis_title='Start Stations',
    yaxis_title='Sum of Trips',
    width=900,
    height=600)
    st.plotly_chart(fig, use_container_width=True)


### Kepler Map

elif page == "Interactive map with aggregated bike trips":
    st.write("Map")
    import os
    path_to_html = "V3_kepler.gl.html"  # Corrected
    print(os.getcwd())
    print(path_to_html)
    with open(path_to_html, 'r') as f:
        html_data = f.read()
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data, height=1000)
    st.markdown("""### This map visualizes the geographic distribution of bike trips, with clusters indicating high-traffic areas that may require additional bikes or rebalancing.""")
    st.markdown("""### Looking at the map, it can be understood that midtown Manhattan has the busiest stations.""")
    
    
if page == "Recommendations":
    st.header("Recommendations for Citi Bikes Resource Allocation")
    st.markdown("""
    Based on the analysis:
    1. **Increase Bike Supply at Top Stations**: Stations like [Station Name] have high demand and should have more bikes allocated.
    2. **Rebalance During Peak Hours**: High trip volumes during [peak hours] suggest rebalancing bikes to high-demand areas in the morning and evening.
    3. **Expand in High-Density Areas**: The map shows clusters in [area]; consider adding new stations or bikes here.
    4. **Monitor Seasonal Trends**: The line chart indicates higher usage in [season], so adjust inventory seasonally.
    """)
