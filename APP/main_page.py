import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import numpy as np
from datetime import datetime
import time
import os

from vessel_alert import create_vessel_document




np.random.seed(42)

# latitude and longitude ranges for the Gulf of Mexico
lat_min, lat_max = 23.0, 28.0
lon_min, lon_max = -95.0, -85.0

# Generate random latitudes and longitudes for vessels
random_latitudes = np.random.uniform(lat_min, lat_max, 12)
random_longitudes = np.random.uniform(lon_min, lon_max, 12)

# DataFrame with vessel coordinates and details
data = pd.DataFrame({
    'MMSI': [123456789, 987654321, 111222333, 222333444, 333444555, 444555666, 555666777,
             666777888, 777888999, 888999111, 999111222, 101112131],
    'LATITUDE': random_latitudes,
    'LONGITUDE': random_longitudes,
    'COURSE': [180, 45, 90, 135, 270, 315, 60, 30, 75, 120, 150, 300],
    'SPEED': [12.5, 15.0, 14.0, 16.0, 13.5, 10.0, 11.0, 12.0, 13.0, 14.5, 15.5, 16.5],
    'HEADING': [180, 45, 90, 135, 270, 315, 60, 30, 75, 120, 150, 300],
    'NAVSTAT': [0] * 12,
    'IMO': [9481494, 9231235, 9452541, 9423567, 9293407, 9347934, 9321234, 
            9439875, 9262339, 9235641, 9295876, 9261234],
    'NAME': ['MSC Gülsün', 'Ever Given', 'Maersk Alabama', 'Emma Maersk', 'CMA CGM Marco Polo', 'Hanjin Europe', 
             'Cosco Development', 'MSC Oscar', 'OOCL Hong Kong', 'Madrid Maersk', 'CMA CGM Jules Verne', 'Hyundai Earth'],
    'CALLSIGN': ['3FWI9', 'VRBH9', 'WDE5165', 'OYYH', 'FAYX', '9V9538', 'VRDE8', 'S9IN', 'VRJH4', 'OXVB', 'FMLC', '9V9713'],
    'FLAG': ['Panama', 'Panama', 'United States', 'Denmark', 'France', 'South Korea', 
             'Hong Kong', 'Panama', 'Hong Kong', 'Denmark', 'France', 'South Korea'],
    'AIS Transponder Class': ['Class A'] * 12,
    'General Vessel Type': ['Cargo Ship', 'Cargo Ship', 'Oil Tanker', 'Passenger Ship', 'Bulk Carrier', 
                            'LNG Carrier', 'Ro-Ro Ship', 'Cargo Ship', 'Bulk Carrier', 'Passenger Ship', 
                            'LPG Carrier', 'Container Ship'],
    'Detailed Vessel Type': ['Container Ship', 'Container Ship', 'VLCC (Very Large Crude Carrier)', 
                             'Cruise Ship', 'Capesize Bulk Carrier', 'LNG Tanker', 
                             'Ro-Ro Vessel', 'Feeder Vessel', 'Handysize Bulk Carrier', 
                             'Ferry', 'LPG Tanker', 'Ultra Large Container Vessel'],
    'A': [50 + i*5 for i in range(12)],
    'B': [120 + i*10 for i in range(12)],
    'C': [20 + i*2 for i in range(12)],
    'D': [18 + i*2 for i in range(12)],
    'DRAUGHT': [5.5 + i*0.1 for i in range(12)],
    'DESTINATION': ['Shanghai', 'Rotterdam', 'Newark', 'Singapore', 'Hamburg', 'Busan', 'Jeddah', 'Antwerp', 
                    'Felixstowe', 'Los Angeles', 'Le Havre', 'Kaohsiung'],
    'LOCODE': ['CNSHA', 'NLRTM', 'USNWK', 'SGSIN', 'DEHAM', 'KRPUS', 'SAJED', 'BEANR', 'GBFXT', 
               'USLAX', 'FRLEH', 'TWKHH'],
    'ETA_AIS': [datetime.utcnow().strftime('%Y-%m-%d %H:%M') for _ in range(12)],
    'ETA': [datetime.utcnow().strftime('%Y-%m-%d %H:%M') for _ in range(12)],
    'ETA_PREDICTED': [datetime.utcnow().strftime('%Y-%m-%d %H:%M') for _ in range(12)],
    'DISTANCE_REMAINING': [100 + i*10 for i in range(12)],
    'SRC': ['SAT'] * 12,
    'ZONE': ['Gulf of Mexico'] * 12,
    'ECA': [False] * 12,
    'TIMESTAMP': [datetime.utcnow()] * 12,
    'STATE': ['green'] * 12 
})


def get_state_html(state):
    color_map = {'green': '#00FF00', 'orange': '#FFA500', 'red': '#FF0000'}
    color = color_map.get(state, '#FFFFFF')
    return f'<div style="width: 20px; height: 20px; border-radius: 50%; background-color: {color}; margin: auto;"></div>'


data['STATE_HTML'] = data['STATE'].apply(get_state_html)

# Sidebar
def sidebar():
    with st.sidebar:
        st.title("Navigation")
        option = st.radio("Go to", ["Home", "Vessel Detail"])
        return option


def main_page():
    st.title("Vessel Tracking Dashboard")

    
    col1, col2 = st.columns([3,2])  

    # Map 
    with col1:
        st.subheader("Vessel Map")
        vessel_map = folium.Map(location=[data['LATITUDE'].mean(), data['LONGITUDE'].mean()], zoom_start=6)
        

        for _, row in data.iterrows():
            color_map = {'green': 'green', 'orange': 'orange', 'red': 'red'}
            color = color_map.get(row['STATE'], 'gray')
            folium.CircleMarker(
                location=[row['LATITUDE'], row['LONGITUDE']],
                radius=8,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                tooltip=f"{row['NAME']}<br>Speed: {row['SPEED']} knots<br>Course: {row['COURSE']} degrees",
            ).add_to(vessel_map)
        
        folium_static(vessel_map)

    # Unicode characters for colored circles
    def get_state_circle(state):
        circle_map = {'green': '🟢', 'orange': '🟠', 'red': '🔴'}
        return circle_map.get(state, '⚪')  


    data['STATE'] = data['STATE'].apply(get_state_circle)

    # Vessel details
    with col2:
        st.subheader("Vessel Details")

        overview_data = data[['STATE', 'NAME', 'IMO', 'MMSI', 'CALLSIGN', 'General Vessel Type']].copy()

        st.dataframe(overview_data)


    additional_details_data = data[['NAME','LATITUDE', 'LONGITUDE', 'General Vessel Type', 'Detailed Vessel Type', 'AIS Transponder Class', 
                                    'COURSE', 'SPEED', 'HEADING', 'NAVSTAT', 'DRAUGHT', 'DESTINATION', 
                                    'LOCODE', 'ETA_AIS', 'ETA_PREDICTED', 'DISTANCE_REMAINING']].copy()

 
    st.subheader("Additional Vessel Details")
    st.dataframe(additional_details_data)
    
    st.subheader("Alert Messages")
    
    simulate_anomaly_detection()

def simulate_anomaly_detection():
    time.sleep(10)
    anomaly_imo = 9481494 
    data['STATE'] = 'green'  
    data.loc[data['IMO'] == anomaly_imo, 'STATE'] = 'orange' 
    
    st.warning(f"Anomaly detected in vessel with IMO {anomaly_imo}.")
    # Create document
    create_vessel_document(data, anomaly_imo)
    st.success("Document has been created.")
    # return True, anomaly_imo  
    st.rerun()
    st.stop()