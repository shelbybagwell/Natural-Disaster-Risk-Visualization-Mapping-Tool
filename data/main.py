from NOAA_API import NOAA_API_Client
from FEMA_API import FEMA_API_Client

def main():

    fema = FEMA_API_Client()

    #Here's the list of datasets that can be pulled from: https://www.fema.gov/about/openfema/data-sets
    #Here are API references such as parameters and structure: https://www.fema.gov/about/openfema/api
    #Here's the specific example below's documentation page: https://www.fema.gov/openfema-data-page/hazard-mitigation-plan-statuses-v1
    r = fema.get_endpoint(version='v1', endpoint='HazardMitigationPlanStatuses')
    status = r['HazardMitigationPlanStatuses']
    print(status[0]) #print first Hazard Mitigation Plan Status

    noaa = NOAA_API_Client()

    #get api info
    noaa.get_api_info()

    #get endpoints
    noaa.get_api_endpoints()

    #getting all state zone ids
    ca_zones = noaa.get_state_zone_ids(state='CA')
    #print(ca_zones)

    #checking alerts for individual zones | CAC036 - no alerts | CAC037 - has alerts
    alerts = noaa.get_alerts_for_zone('CAC036')
    print(alerts)
    alerts = noaa.get_alerts_for_zone('CAC037')
    print(alerts)

    #getting geometry for zones
    geometry_data = noaa.get_endpoint('zones/county/CAC037')
    g = geometry_data['geometry']
    print(g) #cordinates for graphs
    
    #noaa api v2 examples
    locations = noaa.get_endpoint_v2(endpoint='locations')
    locations_metadata = locations['metadata']
    locations_list = locations['results']
    first_location = locations_list[0]
    location_id = first_location['id']
    print(first_location)

    datasets = noaa.get_endpoint_v2(endpoint='datasets', params={'limit': 10, 'offset': 0, 'locationid': location_id})
    datasets_metadata = datasets['metadata']
    datasets_list = datasets['results']
    first_dataset = datasets_list[0]
    dataset_id = first_dataset['id']
    print(first_dataset)

    data = noaa.get_endpoint_v2(endpoint='data', params={'startdate': '2025-01-01', 'enddate': '2025-01-02', 'datasetid': 'GSOM'})
    data_metadata = data['metadata']
    data_list = data['results']
    first_data = data_list[0]
    print(first_data)
    
    datatypes = noaa.get_endpoint_v2(endpoint='datatypes', params={'datasetid': 'GSOM'})
    datatypes_metadata = datatypes['metadata']
    datatypes_list = datatypes['results']
    first_datatype = datatypes_list[0]
    print(first_datatype)

main()