import requests
from django.conf import settings
from api.constants.misc import RELEVANT_FEATURES

# names should be a list of location names, page_size should be an integer >=1, <=200
# start_index should be an integer, result should be a set
def get_placename_matches(names, page_size, start_index, result):
    names_string = ", ".join(names)

    query = {
        "outputFormat": "json",
        "name": names_string,
        "itemsPerPage": page_size,
        "startIndex": start_index,
    }

    try:
        response = requests.get(settings.PLACENAMES_ENDPOINT, params=query)
        response.raise_for_status()
        response = response.json()

        for feature in response["features"]:
            name = feature["properties"]["name"]
            type = feature["properties"]["featureType"]
            if type in RELEVANT_FEATURES:
                result.add(name)

        if response["properties"]["totalResults"] >= start_index + page_size:
            get_placename_matches(names, page_size, start_index + page_size, result)

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
