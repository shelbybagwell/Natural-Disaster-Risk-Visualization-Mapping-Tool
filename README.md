# Natural-Disaster-Risk-Visualization-Mapping-Tool
Wildfire Risk Mapping Tool - an application that ingests data from government organizations such as FEMA and NOAA, and visualizes geographical areas that pose a significant risk of wildfires.

# Installation
- Clone this repository
- Copy the `.env.sample` file to an `.env` file
- From the root directory, run: 
     - `docker compose up -d --build`
- If the container fails to build/run, try rebuilding with the following commands: 
     - `docker compose down -v`
     - `docker system prune -af`
     - `docker compose build --no-cache`
     - `docker compose up -d`

- In the front-end folder, run `npm install` to install the necessary modules, followed by `npm start run` to serve the application

- Flask documentation: 
     - https://pypi.org/project/Flask/

- Flask PyMongo documentation:
     - https://flask-pymongo.readthedocs.io/en/latest/

- PyMongo documentation: 
      - https://pymongo.readthedocs.io/en/stable/