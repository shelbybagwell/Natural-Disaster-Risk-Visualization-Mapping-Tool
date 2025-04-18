import requests


class ESRI_API_Client:
    def __init__(self) -> None:
        self.base_url = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Interagency_Perimeters_Current/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

    def parse_coords(self, coords, bound):
        """
        coords: list of coord pairs - ex:
        """
        north = bound[0]
        south = bound[1]
        east = bound[2]
        west = bound[3]
        keep = False

        for index in coords:
            # lat, lon
            if index[0] < east or index[0] > west:
                if index[1] < north or index[1] > south:
                    keep = True
                    break
        return keep

    def get_data(self, bound=None):
        response = requests.get(self.base_url)
        if response.status_code != 200:
            print(f"Error retrieving data: {response.status_code}")
            return None
        else:
            data = response.json()
            features = [feature for feature in data["features"]]

            bound = [38.09, 32.43, -113.44, -121.50]  # N,S,E,W
            north = bound[0]
            south = bound[1]
            east = bound[2]
            west = bound[3]
            kept_features = []
            for feature in features:
                coords = feature["geometry"]["coordinates"][0]
                coords = [c for c in coords if len(c) == 2]
                lons, lats = zip(*coords)
                min_lon = min(lons)
                max_lon = max(lons)
                min_lat = min(lats)
                max_lat = max(lats)
                if (max_lat < north and min_lat > south) or (
                    max_lon < east and min_lon > west
                ):
                    kept_features.append(feature)
            print(len(features))
            print(len(kept_features))
            return kept_features
