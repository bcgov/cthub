import requests
from django.conf import settings

def get_placename_matches(names_list):
    current_index = 1
    total_results = 200 #temporary
    names_string = ", ".join([str(item) for item in names_list])
    final_community_list = []
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
        "Village (1)",
        "Town"
        ]
    while total_results > current_index:
        data, total_results = get_names_from_api(current_index, total_results, names_string)
        filtered_features = [
        feature for feature in data['features']
        if feature['properties']['featureType'] in features_list
        ]
        for feature in filtered_features:
           final_community_list.append(feature['properties']['name'])
        current_index += 200
    return final_community_list
def get_names_from_api(current_index, total_results, names_string):
    query = {
        'outputFormat': 'json',
        'name' : names_string,
        'itemsPerPage': 200,
        'startIndex': current_index,
        'exactSpelling': 0
        }
    url = settings.PLACENAMES_ENDPOINT
    response = requests.get(url, params=query)
    data = response.json()
    total_results = data['properties']['totalResults']
    return data, total_results
