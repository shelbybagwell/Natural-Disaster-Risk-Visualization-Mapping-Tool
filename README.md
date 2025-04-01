# Natural-Disaster-Risk-Visualization-Mapping-Tool
Wildfire Risk Mapping Tool - an application that ingests data from government organizations such as FEMA and NOAA, and visualizes geographical areas that pose a significant risk of wildfires. This application uses a combination of Angular on the frontend, and Python Flask / PyMongo / MongoDB on the backend.  

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

- Frontend should be accessible via localhost:4200
- Backend should be accessiable via localhost:5000

- Flask documentation: 
     - https://pypi.org/project/Flask/
     - https://flask.palletsprojects.com/en/stable/

- Flask PyMongo documentation:
     - https://flask-pymongo.readthedocs.io/en/latest/

- PyMongo documentation: 
      - https://pymongo.readthedocs.io/en/stable/

- MongoDB documentation: 
     - https://www.mongodb.com/docs/