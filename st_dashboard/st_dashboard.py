import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt

# Configure Streamlit page settings
st.set_page_config(
    page_title="Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

# Add title and descriptive text
st.title("CitiBike 2022 Data Analysis Dashboard")
st.markdown("""
This dashboard provides an interactive interface to explore and visualize data insights.
It includes charts built with Plotly and a geospatial map created with kepler.gl.""")
# Load cleaned data
df = pd.read_csv("df_daily.csv")
top20= pd.read_csv("top20.csv")
import plotly.graph_objects as go

# Create bar chart
st.header("Top 20 Most Popular Bike Stations in New York")
fig = go.Figure(go.Bar(
    x=top20['start_station_name'],
    y=top20['value'],
    marker={'color': top20['value'], 'colorscale': 'Blues'}))
fig.update_layout(title='Top 20 Most Popular Bike Stations in New York',
    xaxis_title='Start Stations',
    yaxis_title='Sum of Trips',
    width=900,
    height=600)
# Display chart in Streamlit
st.plotly_chart(fig)
# Line chart
st.header("Daily Bike Rides and Weather")
fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
fig_2.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['bike_rides_daily'],
        name='Daily Bike Rides',
        marker={'color': 'blue'}),
    secondary_y=False)
fig_2.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['avgWeather'],
        name='Daily Weather',
        marker={'color': 'red'}),
    secondary_y=True)
fig_2.update_layout(
    title='Daily Bike Rides and Weather in New York',
    xaxis_title='Date',
    yaxis_title='Bike Rides',
    yaxis2_title='Weather (°C)',
    height=800)
st.plotly_chart(fig_2, use_container_width=True)
# Add Kepler.gl map
st.header("Bike Trips in New York 2022")
path_to_html = "v2_kepler.gl.html"
with open(path_to_html, 'r') as f:
    html_data = f.read()
st.components.v1.html(html_data, height=1000)
