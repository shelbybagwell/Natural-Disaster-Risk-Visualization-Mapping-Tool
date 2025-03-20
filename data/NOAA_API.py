import requests
import os

class NOAA_API_Client:
    def __init__(self):
        self.base_url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/'
        self.api_key = os.environ.get('NOAA_ACCESS_TOKEN')
        self.headers = {
            "token": self.api_key
        }

    def get_endpoint(self, endpoint='locations', params=None):
        """
            Description:
                This is a general method that can be used to interact with NOAA API Endpoints. It returns the response as a json oject.
                The json object is of a type dict and has the two keys: metadata and results. Here is a link to the documentation for
                each endpoint: https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted
            List of endpoints:
                /datasets
                /datasets/{id}
                /datacategories
                /datacategories/{id}
                /datatypes
                /datatypes/{id}
                /locationcategories
                /locationcategories/{id}
                /locations
                /locations/{id}
                /stations
                /stations/{id}
                /data
            Requirements:
                /data => datasetid, startdate, enddate 
        """
        url = f'{self.base_url}/{endpoint}'
        
        if params is None:
            params = {}

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            print('Error {response.status_code}: {response.text}')
            return None
        else:
            return response.json()
      