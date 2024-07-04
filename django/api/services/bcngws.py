import requests
from django.conf import settings
from api.bcngws_constants import FEATURES


def get_placename_matches(names_list, page_size, start_index, result):
    names_string = ", ".join(map(str, names_list))

    query = {
        'outputFormat': 'json',
        'name': names_string,
        'itemsPerPage': 200,
        'startIndex': start_index,
        'exactSpelling': 0
    }

    try:
        response = requests.get(settings.PLACENAMES_ENDPOINT, params=query)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        response = response.json()

        filtered_names = [
            feature['properties']['name']
            for feature in response['features']
            if feature['properties']['featureType'] in FEATURES.features_list
        ]

        result.extend(filtered_names)

        if response['properties']['totalResults'] >= start_index + page_size:
            get_placename_matches(names_list, page_size, start_index + page_size, result)

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")