import requests
from django.conf import settings

def get_placenames(names_list):
    print('places we are looking for: ' , names_list)
    current_index = 1
    total_results = 200 #temporary
    features_list = [
        "Canadian Forces Base",
        "Canadian Forces Station",
        "City",
        "Community",
        "District Municipality (1)",
        "First Nation Village",
        "Former Locality",
        "Indian Government District",
        "Indian Government District : Land Unit",
        "Indian Reserve-Réserve indienne",
        "Locality",
        "Recreation Facility",
        "Recreational Community",
        "Region",
        "Regional District",
        "Resort Municipality",
        "Urban Community",
        "Village (1)"
        ]
    while total_results > current_index:
        print('current index: ', current_index )
        data, total_results = get_results(current_index, names_list, total_results)
        filtered_features = [
        feature for feature in data['features']
        if feature['properties']['featureType'] in features_list
        ]
        print('total results: ', total_results)
        for feature in filtered_features:
           print(feature['properties']['name'], "-", feature['properties']['featureType'])
        current_index += 200
    print('final_index: ', current_index)
def get_results(current_index, names_list, total_results):
    query = {
        'outputFormat': 'json',
        'name' : names_list,
        'itemsPerPage': 200,
        'startIndex': current_index,
        'exactSpelling': 0
        }
    
    url = settings.PLACENAMES_ENDPOINT
    response = requests.get(url, params=query)
    print(response.url)
    data = response.json()
    total_results = data['properties']['totalResults']
    return data, total_results

    ##"?outputFormat=json&name={}&exactSpelling=0&featureClass=%2A&featureCategory=%2A&featureType=%2A&sortBy=relevance&outputSRS=4326&outputStyle=detail&itemsPerPage=200&startIndex=1".format(names_list)
