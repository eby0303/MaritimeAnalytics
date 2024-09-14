import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import numpy as np
from datetime import datetime
from streamlit_option_menu import option_menu


# Define DataFrame
np.random.seed(42)

# Define latitude and longitude ranges for the Gulf of Mexico
lat_min, lat_max = 23.0, 28.0
lon_min, lon_max = -95.0, -85.0

# Generate random latitudes and longitudes for vessels
random_latitudes = np.random.uniform(lat_min, lat_max, 12)
random_longitudes = np.random.uniform(lon_min, lon_max, 12)

# Create DataFrame with vessel coordinates and details
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
    'STATE': ['green'] * 12  # Initial state for all vessels
})

# Create HTML for the state circles
def get_state_html(state):
    color_map = {'green': '#00FF00', 'orange': '#FFA500', 'red': '#FF0000'}
    color = color_map.get(state, '#FFFFFF')
    return f'<div style="width: 20px; height: 20px; border-radius: 50%; background-color: {color}; margin: auto;"></div>'

# Add STATE_HTML column to DataFrame
data['STATE_HTML'] = data['STATE'].apply(get_state_html)

# Sidebar
def sidebar():
    with st.sidebar:
        st.title("Navigation")
        option = st.radio("Go to", ["Home", "Vessel Detail"])
        return option

# Main page function
def main_page():
    st.title("Vessel Tracking Dashboard")

    # Create two columns with specified widths to avoid intersection
    col1, col2 = st.columns([3, 2])  # Adjust the ratio here (3:2) to control the column widths

    # Map in the first column
    with col1:
        st.subheader("Vessel Map")
        vessel_map = folium.Map(location=[data['LATITUDE'].mean(), data['LONGITUDE'].mean()], zoom_start=6)
        
        # Add vessels to the map
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
        return circle_map.get(state, '⚪')  # Default to a white circle if state isn't mapped

    # Add a visual state circle using Unicode characters
    data['STATE'] = data['STATE'].apply(get_state_circle)

    # Vessel details in the second column using st.dataframe
    with col2:
        st.subheader("Vessel Details")
        # Select the columns for the overview table
        overview_data = data[['STATE', 'NAME', 'IMO', 'MMSI', 'CALLSIGN', 'General Vessel Type']].copy()

        # Display the table using st.dataframe for interactive features
        st.dataframe(overview_data)

    # Additional vessel details to be displayed in a second table
    additional_details_data = data[['NAME','LATITUDE', 'LONGITUDE', 'General Vessel Type', 'Detailed Vessel Type', 'AIS Transponder Class', 
                                    'COURSE', 'SPEED', 'HEADING', 'NAVSTAT', 'DRAUGHT', 'DESTINATION', 
                                    'LOCODE', 'ETA_AIS', 'ETA_PREDICTED', 'DISTANCE_REMAINING']].copy()

    # Display the additional table below the first one
    st.subheader("Additional Vessel Details")
    st.dataframe(additional_details_data)

# Vessel detail page function
def vessel_detail_page():
    # Get the vessel name from the user input
    selected_name = st.selectbox("Select a Vessel", data['NAME'])
    
    # Filter the data for the selected vessel
    vessel_data = data[data['NAME'] == selected_name].iloc[0]

    st.title(f"Vessel Detail: {selected_name}")

    # Create a container for vessel details
    with st.container():
        st.subheader("Vessel Overview")
        
        # Use columns for a clean layout
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
        
        # Display voyage-related details
        st.write(f"**Destination:** {vessel_data['DESTINATION']}")
        st.write(f"**LOCODE:** {vessel_data['LOCODE']}")
        st.write(f"**ETA (AIS):** {vessel_data['ETA_AIS']}")
        st.write(f"**ETA (Predicted):** {vessel_data['ETA_PREDICTED']}")
        st.write(f"**Distance Remaining:** {vessel_data['DISTANCE_REMAINING']} nautical miles")
        
        # Create a Folium map centered on the vessel's location
    vessel_map = folium.Map(location=[vessel_data['LATITUDE'], vessel_data['LONGITUDE']], zoom_start=10)

    # Add a marker for the selected vessel
    folium.Marker(
        location=[vessel_data['LATITUDE'], vessel_data['LONGITUDE']],
        popup=folium.Popup(f"{selected_name}<br>Speed: {vessel_data['SPEED']} knots<br>Course: {vessel_data['COURSE']} degrees", max_width=300),
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(vessel_map)

    # Display the map in Streamlit
    folium_static(vessel_map)

# Main function to control page routing
def main():
    with st.sidebar:
        st.sidebar.title("Vessel Tracking Dashboard")

        # The options
        options = ["Home", "Vessel Details"]

        # Selectbox for menu
        selected = option_menu(
            menu_title="Navigation",
            options=options,
            # icons=["house", "ship"],
            menu_icon="cast",
            default_index=0,
            orientation="vertical"
        )

    # Handle page selection
    if selected == "Home":
        main_page()  # Call the function for the main page
    elif selected == "Vessel Details":
        vessel_detail_page()  # Call the function for the vessel details page

if __name__ == "__main__":
    main()
