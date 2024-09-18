import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import numpy as np
from datetime import datetime




np.random.seed(42)

# latitude and longitude ranges for the Gulf of Mexico
lat_min, lat_max = 23.0, 28.0
lon_min, lon_max = -95.0, -85.0


random_latitudes = np.random.uniform(lat_min, lat_max, 12)
random_longitudes = np.random.uniform(lon_min, lon_max, 12)


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








def vessel_detail_page():
    
    selected_name = st.selectbox("Select a Vessel", data['NAME'])
    
   
    vessel_data = data[data['NAME'] == selected_name].iloc[0]

    st.title(f"Vessel Detail: {selected_name}")

    
    with st.container():
        st.subheader("Vessel Overview")
        
       
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**IMO:** {vessel_data['IMO']}")
            st.write(f"**MMSI:** {vessel_data['MMSI']}")
            st.write(f"**Callsign:** {vessel_data['CALLSIGN']}")
            st.write(f"**Flag:** {vessel_data['FLAG']}")
            st.write(f"**General Vessel Type:** {vessel_data['General Vessel Type']}")
            st.write(f"**Detailed Vessel Type:** {vessel_data['Detailed Vessel Type']}")
        
        with col2:
            st.write(f"**AIS Transponder Class:** {vessel_data['AIS Transponder Class']}")
            st.write(f"**Course:** {vessel_data['COURSE']} degrees")
            st.write(f"**Speed:** {vessel_data['SPEED']} knots")
            st.write(f"**Heading:** {vessel_data['HEADING']} degrees")
            st.write(f"**Navigation Status:** {vessel_data['NAVSTAT']}")
            st.write(f"**Draught:** {vessel_data['DRAUGHT']} meters")
        
        st.subheader("Voyage Information")
        st.write(f"**Destination:** {vessel_data['DESTINATION']}")
        st.write(f"**LOCODE:** {vessel_data['LOCODE']}")
        st.write(f"**ETA (AIS):** {vessel_data['ETA_AIS']}")
        st.write(f"**ETA (Predicted):** {vessel_data['ETA_PREDICTED']}")
        st.write(f"**Distance Remaining:** {vessel_data['DISTANCE_REMAINING']} nautical miles")
        

    vessel_map = folium.Map(location=[vessel_data['LATITUDE'], vessel_data['LONGITUDE']], zoom_start=10)

    # Marker for selected vessel
    folium.Marker(
        location=[vessel_data['LATITUDE'], vessel_data['LONGITUDE']],
        popup=folium.Popup(f"{selected_name}<br>Speed: {vessel_data['SPEED']} knots<br>Course: {vessel_data['COURSE']} degrees", max_width=300),
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(vessel_map)


    folium_static(vessel_map)