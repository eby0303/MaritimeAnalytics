# # Automated Vessel Anomaly and Oil Spill Detection System

This project aims to create a real-time vessel tracking system with anomaly detection and oil spill identification using AIS data and satellite imagery.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview
This project combines real-time vessel tracking data with satellite imagery to detect anomalies in vessel behavior and identify potential oil spills in maritime regions. The system automates the monitoring process, enabling early detection of environmental hazards and enabling timely responses.

![Dashboard Preview](https://github.com/user-attachments/assets/0f579425-1b52-4bbb-a4d1-18d326d24004)
)

## Features
- **AIS Data Integration**: Real-time vessel tracking based on AIS data (Automatic Identification System).
- **Anomaly Detection**: Identify anomalies in vessel behavior based on speed, course, or navigation patterns.
- **Satellite Imagery Analysis**: High-resolution satellite imagery from Sentinel Hub is used for detecting potential oil spills.
- **Real-Time Monitoring**: Continuous monitoring of vessels and the surrounding water for quick detection of incidents.
- **Early Warning System**: Automated alerts when anomalies or oil spills are detected.
  
## Technologies Used
- **Python**: For back-end logic and anomaly detection algorithms.
- **Streamlit**: For building the interactive web dashboard.
- **Sentinel Hub API**: For accessing satellite imagery.
- **AIS Data**: Used for real-time vessel tracking and movement analysis.
- **Folium/Leaflet Maps**: For plotting vessel positions on interactive maps.

## Setup
To run this project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/vessel-anomaly-detection.git
    cd vessel-anomaly-detection
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python -m venv env
    source env/bin/activate   # On Windows, use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Set up API keys for AIS data and Sentinel Hub:
    - Obtain your **AIS API Key** and **Sentinel Hub API Key**.
    - Add them to a `.env` file:
    ```
    AIS_API_KEY=your_ais_api_key
    SENTINEL_HUB_API_KEY=your_sentinel_hub_api_key
    ```

4. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Usage
Once the app is running, you can monitor vessels in real time on the map. The system will highlight:
- **Green dots**: Normal vessel behavior (no anomalies).
- **Orange dots**: 2 detected anomalies.
- **Red dots**: 4 or more anomalies detected, indicating a high-risk situation.
- The satellite imagery analysis will also indicate potential oil spill zones, enabling further monitoring.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new feature branch.
3. Submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
