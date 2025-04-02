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
        self.tag_prefix = r'{http://earth.google.com/kml/2.1}'

    def parse_kml(serlf, kml_data):
        root = parser.parse(io.BytesIO(kml_data)).getroot()
        return root
    
    def tag(self, tag=None):
        """
            Description:
                This is just a utility function so we don't have to keep typing the long prefix and can just pass tag names
        """
        return self.tag_prefix + tag

    def get_immediate_children(self, elem_tree=None):
        """
            Description:
                This function will take an XML Tree and return a list of the next immediate children tags
        """
        if elem_tree == None:
            return None
    
        children = elem_tree.findall('*')
        
        return [x.tag.replace(self.tag_prefix, '') for x in children]

    def get_file_info(self, elem_tree=None):
        """
            Description:
                This function will return the intial folder with the file info
        """
        if elem_tree == None:
            return None
        
        document = elem_tree.find(self.tag('Document'))
        name = document.find(self.tag('name'))
        description = document.find(self.tag('description'))
        lookAt = document.find(self.tag('LookAt'))
        region = document.find(self.tag('Region'))
        
        info = {
            "Name": name.text,
            "Description": description.text,
            "LookAt": lookAt.text.replace('\n', '').replace(' ', ''),
            "Region": region.text.replace('\n', '').replace(' ', '')
        }

        return info

    def get_file_data(self, elem_tree=None):
        """
            Description:
                This function loops through all the folders in the xml and parses and transforms the data into a dict/json format. It returns a list of dictionaries that appear as such:
                {
                    'name': 'name',
                    'placemarker': [...],
                    'ScreenOverlay' : '', (this is only if it has it, the intial legend and logos folder does)
                }
        """
        
        if elem_tree == None:
            return None
        
        document = elem_tree.find(self.tag('Document')) #need to step inside the kml tag into the document tag that holds everything
        folders = document.findall(self.tag('Folder')) # these are all the folder tags returned into a list

        data = []
        
        for f in folders: #loops through high level overview of folder elements each one contains elements pertaining name, placemark, etc

            elements = self.get_immediate_children(f) 
            e_dict = {}
            placemark_list = []
            for e in elements: #loop through the elements in the folder element (name, placemark, etc)

                if e != 'Placemark': #essentailly all the placemarks are the individual markers/items we want so combine those by folder and contain them in a list so we're handling them in the else statement
                    child = f.find(self.tag(e))
                    match e: #specific formatting for each element tag
                        case 'name':
                            e_dict[e] = child.text.strip()
                        case 'ScreenOverlay':
                            e_dict[e] = child.text.replace(' ', '').replace('\n', '')
                        case _:
                            e_dict[e] = child.text
                else:
                    if placemark_list != []:
                        break

                    placemarkers = f.findall(self.tag(e)) #Get all placemarker elements
                    for p in placemarkers:
                        p_elements = self.get_immediate_children(p)
                        i_dict = {}
                        for ele in p_elements: #loop through the placemarker element and its children ex. description, point, polygon, etc...
                            p_child = p.find(self.tag(ele))
                            match ele:
                                case 'description':
                                    desc = {}
                                    desc_text = p_child.text.replace('<b>', '').replace('</b>', '').replace('<br/>', '').replace(' ', '').replace('\n\n', '')
                                    desc_split = [desc.split(':') for desc in desc_text.split('\n')]
                                    for de in desc_split:
                                        desc[de[0]] = de[1]

                                    i_dict[ele] = desc
                                case 'Point':
                                    coords = p_child.find(self.tag('coordinates')).text.split(',')
                                    i_dict[ele] = coords
                                case 'Polygon':
                                    points = p_child.find(self.tag('outerBoundaryIs')).find(self.tag('LinearRing')).find(self.tag('coordinates')).text.replace(' ', '').replace('\n\n', '')
                                    points = [p for p in points.split('\n') if p != '']
                                    pc = {}
                                    for q in range(len(points)):
                                        pc[q] = points[q].split(',')
                                    i_dict[ele] = pc
                                case _: #default if isn't listed
                                    i_dict[ele] = str(p_child.text).replace(' ', '').replace('\n', '')

                        placemark_list.append(i_dict) #append this specific i_dict for one placemarker to the list so we can include all of them under the placemarker key in the main dictionary

            e_dict['Placemark'] = placemark_list #include list of placemarkers for folder into the main dictionary
            data.append(e_dict) #append the main dictionary holding all the information for the specific folder to the data list

        return data


    def get_data(self, sensor=Sensor.MODIS, region="usa_contiguous_and_hawaii", time="24h"):
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
