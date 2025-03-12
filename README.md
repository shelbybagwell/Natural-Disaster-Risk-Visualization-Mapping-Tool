# Natural-Disaster-Risk-Visualization-Mapping-Tool
Wildfire Risk Mapping Tool - an application that ingests data from government organizations such as FEMA and NOAA, and visualizes geographical areas that pose a significant risk of wildfires.

# Installation
- Clone this repository
- Copy the `.env.sample` file to an `.env` file
- From the root directory, run: 
     - `docker compose up -d --build`
- If the front-end will not load, try running `npm install` from within the container:
    - `docker exec -it angular_container sh`
    - `npm cache clean --force`
    - `npm install`