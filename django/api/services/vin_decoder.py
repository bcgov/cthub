import logging
import requests
import json

from api.models.icbc_registration_data import IcbcRegistrationData
from rest_framework.response import Response
from django.core.paginator import Paginator

def decoder():
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/'
    
    json_response = None
    vin_queryset = IcbcRegistrationData.objects.values_list('vin', flat=True).order_by('vin')
    pages = Paginator(vin_queryset, 50)
    #for p in pages:
    page = pages.page(1)
    vin_batch = ';'.join( page.object_list )
    post_fields = {'format': 'json', 'data': vin_batch}
    try:
        response = requests.post(url, data=post_fields)
        if not response.status_code == 200:
            LOGGER.error("Error: Decoding Failed! %s", response)
            return
        json_response = response.json()
        # decoded_result.append(json_response)
    except requests.exceptions.RequestException as e:
        LOGGER.error("Error: {}".format(e))
        return

    return json_response

