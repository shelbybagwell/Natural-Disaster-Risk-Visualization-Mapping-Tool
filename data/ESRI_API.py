import requests


class ESRI_API_Client:
    def __init__(self) -> None:
        self.base_url = (
            "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/"
        )
