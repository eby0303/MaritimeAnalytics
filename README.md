# # Automated Vessel Anomaly and Oil Spill Detection System

## THIS IS A PROTOTYPE
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


## Features
- **AIS Data Integration**: Real-time vessel tracking with key details like speed, course, MMSI, and position.
- **Anomaly Detection**: Automatically detects vessel movement anomalies such as:
  - Deviation from expected course
  - Unusual speed fluctuations
  - Course correction delays
- **Satellite Imagery Integration**: Uses Sentinel Hub high-resolution imagery to detect potential oil spills.
- **Automated Alerts**: Alerts when anomalies or potential spills are detected for rapid response.
- **Comprehensive Dashboard**: Visualize vessel positions, statuses, and anomalies on an interactive map.

## Proposed Solution/Prototype:
1. **AIS Data Integration**: Real-time updates on vessel tracking using AIS data to monitor vessel positions and movements.
2. **Satellite Imagery**: High-resolution imagery from Sentinel Hub is used to identify oil spills, ensuring continuous surveillance of critical waters.
3. **Real-Time Anomaly Detection**: Monitors vessel movements for anomalies such as irregular speed, changes in course, and other unusual activities.
4. **Oil Spill Detection**: Identifies oil spills based on satellite imagery combined with vessel data, enabling timely interventions.
5. **Early Detection Mechanism**: The system enables early identification of oil spills or vessel anomalies for rapid response and mitigation.
6. **Automated Monitoring**: The process is fully automated, integrating vessel tracking and satellite imagery for real-time monitoring.

## Technology Stack
- **Frontend**: Streamlit for interactive dashboards
- **Backend**: Python with Flask
- **Database**: MySQL (for AIS data storage)
- **Vessel Tracking**: AIS API for real-time vessel movement data
- **Satellite Imagery**: Sentinel Hub API for oil spill detection
- **Mapping**: Folium and Streamlit Map integration
- **Deployment**: Docker, AWS for cloud hosting


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
