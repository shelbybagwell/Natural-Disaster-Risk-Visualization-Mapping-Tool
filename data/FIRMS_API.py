import io
import requests
import os
import zipfile
from fastkml import kml
from pykml import parser
import xml.etree.ElementTree as ET


class Sensor:
    MODIS = "c6.1"
    S_NPP = "suomi-npp-viirs-c2"
    NOAA20 = "noaa-20-viirs-c2"
    NOAA21 = "noaa-21-viirs-c2"
    LANDSAT = "landsat"


class FIRMS_API_Client:
    def __init__(self) -> None:
        self.base_url = "https://firms.modaps.eosdis.nasa.gov/api/kml_fire_footprints"
        self.data_dir = os.getcwd()

    def parse_kml(serlf, kml_data):
        root = parser.parse(io.BytesIO(kml_data)).getroot()
        return root

    def get_data(
        self, sensor=Sensor.MODIS, region="usa_contiguous_and_hawaii", time="24h"
    ):
        url = f"{self.base_url}/{region}/{time}/{sensor}"
        print(url)

        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error retrieving data: {response.status_code}")
            return None
        else:
            response.encoding = "utf-8"
            if "application/vnd.google-earth.kmz" in response.headers.get(
                "Content-Type", ""
            ):
                with zipfile.ZipFile(io.BytesIO(response.content), "r") as kmz:
                    kml_filename = [
                        name for name in kmz.namelist() if name.endswith(".kml")
                    ][0]
                    with kmz.open(kml_filename) as kml_file:
                        kml_string = kml_file.read().decode("utf-8")
            else:
                kml_string = response.text
            root = ET.fromstring(kml_string)
            placemarks = []
            print(root.findall("Placemark"))
            for PM in root.findall(".//{http://www.opengis.net/kml/2.2}Placemark"):
                print(PM)
                name = (
                    PM.find("{http://www.opengis.net/kml/2.2}name").text
                    if PM.find("{http://www.opengis.net/kml/2.2}name") is not None
                    else "Unnamed"
                )
                coordinates = PM.find(".//{http://www.opengis.net/kml/2.2}coordinates")

                if coordinates is not None:
                    coords = coordinates.text.strip()
                else:
                    coords = "No coordinates"

                placemarks.append({"name": name, "coordinates": coords})
            print(placemarks)
            return response.status_code
