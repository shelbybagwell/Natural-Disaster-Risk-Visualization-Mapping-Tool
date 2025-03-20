import requests
import os

class NOAA_API_Client:
    def __init__(self):
        self.base_url = 'https://api.weather.gov/'
        self.base_url_v2 = 'https://www.ncei.noaa.gov/cdo-web/api/v2/'
        self.api_key = os.environ.get('NOAA_ACCESS_TOKEN')
        self.headers = {
            "token": self.api_key
        }

    def get_api_info(self):

        response = requests.get(self.base_url + 'openapi.json')
        info = response.json()

        if response.status_code != 200:
            print(f'Error {response.status_code}: {response.text}')
        else:
            print('Version: ', info['openapi'])
            print('Info: ', info['info'])
            print('Server: ' , info['servers'])
            print('Security: ', info['security'])
            print('Documentation: ', info['externalDocs'])

    def get_api_endpoints(self):

        response = requests.get(self.base_url + 'openapi.json')
        info = response.json()

        if response.status_code != 200:
            print(f'Error {response.status_code}: {response.text}')
        else:
            paths = info['paths']
            for p in paths.keys():
                print(p + ' - ' + paths[p]['get']['description'])

    def get_endpoint(self, endpoint='zones', params=None):
        """
            Description:
                This is to utilize the API, https://api.weather.gov/. There are a lot of endpoints that are accessible.
                Use the get_api_endpoints() method to get their names and descriptions
        """
        url = f'{self.base_url}/{endpoint}'
        
        if params is None:
            params = {}

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            print(f'Error {response.status_code}: {response.text}')
            return None
        else:
            return response.json()

    def get_state_zone_ids(self, state='TN', params=None):
        zones_info = self.get_endpoint('zones')
        zones = zones_info['features']
        state_zones = []
        for z in zones:
            properties = z['properties']
            id = properties['id']
            st = properties['state']
            if st == state:
                state_zones.append(id)

        return state_zones

    def get_alerts_for_zone(self, zone_id, params=None):

        if zone_id == None:
            print('Zone ID Required.')
            return False
        
        alert_info = self.get_endpoint(endpoint=f'alerts/active/zone/{zone_id}')

        if alert_info['features'] == []:
            return f'{zone_id}: No Alerts, Last Updated: ' + alert_info['updated']
        else:
            alerts = []
            for i in alert_info['features']:
                properties = i['properties']
                alert = {
                    'zone_id': zone_id,
                    '@id': properties['@id'],
                    '@type': properties['@type'],
                    'id': properties['id'],
                    'areaDesc': properties['areaDesc'],
                    'geocode': properties['geocode'],
                    'affectedZones': properties['affectedZones'],
                    'references': properties['references'],
                    'sent': properties['sent'],
                    'effective': properties['effective'],
                    'onset': properties['onset'],
                    'expires': properties['expires'],
                    'ends': properties['ends'],
                    'status': properties['status'],
                    'messageType': properties['messageType'],
                    'category': properties['category'],
                    'severity': properties['severity'],
                    'certainty': properties['certainty'],
                    'urgency': properties['urgency'],
                    'event': properties['event'],
                    'sender': properties['sender'],
                    'senderName': properties['senderName'],
                    'headline': properties['headline'],
                    'description': properties['description'],
                    'instruction': properties['instruction'],
                    'response': properties['response'],
                    'parameters': properties['parameters'],
                    'lastUpdated': alert_info['updated'],
                    'title': alert_info['title']
                }
                alerts.append(alert)

            return alerts

    def get_endpoint_v2(self, endpoint='locations', params=None):
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
        url = f'{self.base_url_v2}/{endpoint}'
        
        if params is None:
            params = {}

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            print(f'Error {response.status_code}: {response.text}')
            return None
        else:
            return response.json()
      