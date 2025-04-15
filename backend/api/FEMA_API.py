import requests

class FEMA_API_Client:
    def __init__(self):
        self.base_url = 'https://www.fema.gov/api/open'

    def get_endpoint(self, version='v1', endpoint='v1', params=None):
        """
           Versions: v1, v2, v3, v4
           Endpoint = Entity's Name
        """
        url = f'{self.base_url}/{version}/{endpoint}'
        print(url)
        
        if params is None:
            params = {}

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f'Error {response.status_code}: {response.text}')
            return None
        else:
            return response.json()
      