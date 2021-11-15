import logging
import requests
import json

from api.models.icbc_registration_data import IcbcRegistrationData
from api.models.vin_decoded_information import VINDecodedInformation
from rest_framework.response import Response
from django.core.paginator import Paginator

LOGGER = logging.getLogger(__name__)

def decoder():
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/'
    json_response = None
    model_year = None
    vin_queryset = IcbcRegistrationData.objects.values_list('vin', flat=True).order_by('vin')
    pages = Paginator(vin_queryset, 50)
    # Remove commented out code to decode all the VINs inside icbc registration data table
    #for p in pages:
    page = pages.page(1) #replace 1 with p.number
    vin_batch = ';'.join( page.object_list )
    post_fields = {'format': 'json', 'data': vin_batch}
    try:
        response = requests.post(url, data=post_fields)
        if not response.status_code == 200:
            LOGGER.error("Error: Decoding Failed! %s", response)
            return

        json_response = response.json()
        results = json_response['Results']
        if results:
            for item in results:
                if item['ModelYear']:
                    model_year = int(item['ModelYear']) 
                VINDecodedInformation.objects.create(
                    manufacturer=item['Manufacturer'],
                    make=item['Make'],
                    model=item['Model'],
                    model_year=model_year,
                    fuel_type_primary=item['FuelTypePrimary']
                )
    except requests.exceptions.RequestException as e:
        LOGGER.error("Error: {}".format(e))
        return

    return

