import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import numpy as np
from datetime import datetime
from streamlit_option_menu import option_menu
import time

from main_page import main_page, simulate_anomaly_detection
from vessel_detail import vessel_detail_page
from vessel_alert import document_viewer
from satelliteimages import satellite_images


# Sidebar
def sidebar():
    with st.sidebar:
        st.title("Navigation")
        option = st.radio("Go to", ["Home", "Vessel Detail","Vessel Alert Docs"])
        return option


# Main function to control page routing
def main():
    with st.sidebar:
        st.sidebar.title("Vessel Tracking Dashboard")

        # The options
        options = ["Home", "Vessel Details","Vessel Alert Docs","Satellite Images"]

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
    elif selected == "Vessel Alert Docs":
        document_viewer()
    elif selected == "Satellite Images":
        satellite_images()
        
if __name__ == "__main__":
    main()
