import streamlit as st
from PIL import Image
from sentinelhub import BBox, CRS
from config import get_sentinelhub_config
from scripts.ship_detection_rgb import get_ship_detection_rgb_image
from scripts.oil_spill_detection_rgb import get_oil_spill_detection_rgb_image
from scripts.get_true_color_image import get_true_color_image
from scripts.get_sar_image import get_sar_image


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



def satellite_images():
    selected_name = st.selectbox("Select a Vessel", data['NAME'])
    
   
    vessel_data = data[data['NAME'] == selected_name].iloc[0]
    vessel_lat = vessel_data["LATITUDE"]
    vessel_lon = vessel_data["LONGITUDE"]
    
    with st.container():
        st.title(f"Vessel Detail: {selected_name}")
        
        if vessel_lat and vessel_lon:
            try:
                vessel_lat, vessel_lon = float(vessel_lat), float(vessel_lon)
                bbox = BBox([vessel_lon - 0.1, vessel_lat - 0.1, vessel_lon + 0.1, vessel_lat + 0.1], CRS.WGS84)
                st.write(f"Selected location: ({vessel_lat}, {vessel_lon})")

                # True Color Satellite Image
                st.subheader("True-Color Satellite Image")
                true_color_img = get_true_color_image(bbox)
                if true_color_img:
                    st.image(true_color_img, caption="True-Color Satellite Image", use_column_width=True)
                else:
                    st.write("No satellite image data available for this location.")

                # SAR Image
                st.subheader("SAR Satellite Image")
                sar_img = get_sar_image(bbox)
                if sar_img:
                    st.image(sar_img, caption="SAR Image (VV/VH)", use_column_width=True)
                else:
                    st.write("No SAR image data available for this location.")

                # Ship Detection (RGB Ratio)
                st.subheader("Ship Detection (RGB Ratio)")
                ship_img_rgb = get_ship_detection_rgb_image(bbox)
                if ship_img_rgb:
                    st.image(ship_img_rgb, caption="RGB Ratio for Ship Detection", use_column_width=True)
                else:
                    st.write("No ship data available for this location.")

                # Oil Spill Detection (RGB Ratio)
                st.subheader("Oil Spill Detection (RGB Ratio)")
                oil_img_rgb = get_oil_spill_detection_rgb_image(bbox)
                if oil_img_rgb:
                    st.image(oil_img_rgb, caption="RGB Ratio for Oil Spill Detection", use_column_width=True)
                else:
                    st.write("No oil spill data available for this location.")

            except ValueError:
                st.write("Invalid latitude/longitude input. Please enter valid numbers.")

        
        

    
    
    
    

