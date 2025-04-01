import requests


class ESRI_API_Client:
    def __init__(self) -> None:
        self.base_url = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Interagency_Perimeters_Current/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

    def get_data(self):
        response = requests.get(self.base_url)
        if response.status_code != 200:
            print(f"Error retrieving data: {response.status_code}")
            return None
        else:
            data = response.json()
            features = [feature for feature in data["features"]]
            print(len(features[0]["geometry"]["coordinates"][0]))
            return data
