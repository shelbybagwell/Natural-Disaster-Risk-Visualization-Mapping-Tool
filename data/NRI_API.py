import requests
import os
from urllib.parse import urlencode

"""
Lightbox API National Risk Index Client
Documentation: https://developer.lightboxre.com/api/femarisks

"""

class NRI_API_Client:

    base_url = ''
    api_key = ''

    def __init__(self):

        """
        LIGHTBOX_API_KEY must be included in .env 
        """

        self.base_url = 'https://api.lightboxre.com/v1/riskindexes'
        self.api_key = os.environ.get('LIGHTBOX_API_KEY')

        # print(self.api_key)

        self.headers = {
            "x-api-key": f"{self.api_key}",
            "accept": "application/json",
        }

    def get_endpoint(self, endpoint='', params=None):

        """
            List of Endpoints:
            General: GET {base_url}/us/{id} (default) Query for a specific national risk index records using the risk index unique 'ID.'
            Address: GET {base_url}address/search?{params}  Query for a specific national risk index records by property address.
            Spatial: GET {base_url}/us/geometry?wkt={POINT(long,lat)}
                     GET {base_url}/us/geometry?wkt={LINESTRING(start_long,start_lat,end_long,end_lat)}
                     GET {base_url}/us/geometry?wkt={POLYGON(([multiple_coordinates]))}
        """

        try :

            if (endpoint is None or endpoint == ''):
                raise "Endpoint not specified"

            url = f'{self.base_url}/{endpoint}'

            if params is None:
                params = {}
            else:
                params = urlencode(params)

            print(url)
            print(params)

            response = requests.get(url, headers=self.headers, params=params)

            # print(f'{response.status_code}: {response.text}')
            
            # Handle response
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                print("Bad request (check your point/coordinate syntax)")
            elif response.status_code == 401:
                print("Unauthorized (check API key)")
            elif response.status_code == 404:
                print("Not found (check endpoint or coordinates)")
            elif response.status_code == 500:
                print("Internal server error")
            else:
                print(f"Unexpected error: {response.status_code}: {response.text}")

        except requests.RequestException as ex:
            print(f"Network error: {ex}")
        except Exception as ex:
            print('{ex}')

        return None
    

    def test_cases(self):

        # General (uses unique ID of area)
        # self.get_endpoint('us/T06037207400') # Los Angeles (34.0549° N, 118.2426° W)
        # self.get_endpoint('us/T37183050100') # Raleigh, NC (35.7796° N, 78.6382° W)
        # self.get_endpoint('us/T48065950200') # Texas Panhandle (35.3456° N, 101.3804° W)

        # Spatial (uses lat/long coordinates)

        # Los Angeles (currently no wildfire risk)
        # params = {
        #     'wkt' : 'POINT(-118.2437 34.0522)',
        #     'bufferDistance' : 50, 
        #      'bufferUnit' : 'm'
        #     }
        
        # self.get_endpoint('us/geometry', params) 

        # Texas Panhandle (current ongoing wildfire risk)
        params = {
            'wkt' : 'POINT(-101.3804 35.3456)', 
            'bufferDistance' : 50, 
             'bufferUnit' : 'm'
            }
        
        texas_wildfire_status = self.get_endpoint('us/geometry', params) 

        if texas_wildfire_status:
            print(texas_wildfire_status['nris'][0]['wildfire']['hazardTypeRiskIndex'])


# if __name__ == "__main__":

#     obj = NRI_API_Client()
#     obj.test_cases()
