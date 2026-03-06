import folium
import streamlit as st
from streamlit_folium import st_folium
import requests
from datetime import datetime
import pandas as pd

'''
# TaxiFare
'''

st.write("Enter your location and the passenger count:")
# Date and time
trip_datetime = st.datetime_input(
    "Pickup Date and Time",
    value=datetime.now()
)
# Pickup coordinates
pickup_lat = st.number_input("Pickup Latitude", value=48.8566)
pickup_lon = st.number_input("Pickup Longitude", value=2.3522)
# Dropoff coordinates
dropoff_lat = st.number_input("Dropoff Latitude", value=48.8666)
dropoff_lon = st.number_input("Dropoff Longitude", value=2.3622)
# Passenger count
passenger_count = st.number_input(
    "Passenger Count",
    min_value=0,value=1)

# Design the map, plot the map
pickup = [pickup_lat, pickup_lon]
dropoff = [dropoff_lat, dropoff_lon]

center_lat = (pickup[0] + dropoff[0]) / 2
center_lon = (pickup[1] + dropoff[1]) / 2

# Create map centered and zoomed
m = folium.Map(location=[center_lat, center_lon],
               zoom_start=14, tiles="CartoDB dark_matter")

# Pickup point
folium.CircleMarker(
    location=pickup,
    radius=6,               # point size
    color="white",          # border color
    fill=True,              # enable fill
    fill_color="#09E0E0",     # fill color
    fill_opacity=0.8,
    tooltip="Pickup"
).add_to(m)

# Dropoff point
folium.CircleMarker(
    location=dropoff,
    radius=6,
    color="white",
    fill=True,
    fill_color="#09E0E0",
    fill_opacity=0.8,
    tooltip="Dropoff"
).add_to(m)

folium.PolyLine([pickup, dropoff], color="#09E0E0",
                dash_array="5, 10", weight=3).add_to(m)

st_folium(m, width=750, height=500)

'''
## Validate when informations ready:
'''

url = 'http://127.0.0.1:8000/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')


if st.button("Validate"):

    params = {
        "pickup_datetime": trip_datetime.isoformat(),
        "pickup_latitude": pickup_lat,
        "pickup_longitude": pickup_lon,
        "dropoff_latitude": dropoff_lat,
        "dropoff_longitude": dropoff_lon,
        "passenger_count": passenger_count
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        result = response.json()
        fare = round(result['fare'],2)
        st.write(f"Estimated fare : ${fare}")

    else:
        st.error(f"API Error: {response.status_code}")
        st.text(response.text)
