from NOAA_API import NOAA_API_Client

def main():
    noaa = NOAA_API_Client()

    locations = noaa.get_endpoint(endpoint='locations')
    locations_metadata = locations['metadata']
    locations_list = locations['results']
    first_location = locations_list[0]
    location_id = first_location['id']
    print(first_location)

    datasets = noaa.get_endpoint(endpoint='datasets', params={'limit': 10, 'offset': 0, 'locationid': location_id})
    datasets_metadata = datasets['metadata']
    datasets_list = datasets['results']
    first_dataset = datasets_list[0]
    dataset_id = first_dataset['id']
    print(first_dataset)

    data = noaa.get_endpoint(endpoint='data', params={'startdate': '2025-01-01', 'enddate': '2025-01-02', 'datasetid': 'GSOM'})
    data_metadata = data['metadata']
    data_list = data['results']
    first_data = data_list[0]
    print(first_data)
    
    datatypes = noaa.get_endpoint(endpoint='datatypes', params={'datasetid': 'GSOM'})
    datatypes_metadata = datatypes['metadata']
    datatypes_list = datatypes['results']
    first_datatype = datatypes_list[0]
    print(first_datatype)


main()