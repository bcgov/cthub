import json
import logging
import requests

from django.core.paginator import Paginator
from django.conf import settings

from api.models.icbc_registration_data import IcbcRegistrationData
from api.models.vin_decoded_information import VINDecodedInformation

LOGGER = logging.getLogger(__name__)


def parse_vin(vin, item):
    us_market_data = item.get('us_market_data')
    common_data = us_market_data.get('common_us_data')
    if common_data is None:
        supplemental_data = item.get('supplemental_data')
        common_data = supplemental_data.get('common_supplemental_data')

    basic_data = common_data.get('basic_data')
    engines = common_data.get('engines')

    model_year = None
    if basic_data.get('year'):
        model_year = int(basic_data.get('year'))

    query_error = item.get('query_error')

    if query_error.get('error_code') == '' and len(engines) > 0:
        return VINDecodedInformation.objects.create(
            fuel_type_primary=engines[0].get('fuel_type'),
            make=basic_data.get('make'),
            manufacturer=basic_data.get('country_of_manufacture'),
            model_year=model_year,
            model=basic_data.get('model'),
            vin=vin
        )

    return None


def decoder():
    url = 'https://api.dataonesoftware.com/webservices/vindecoder/decode'
    json_response = None

    vin_queryset = IcbcRegistrationData.objects.values_list(
        'vin', flat=True
    ).order_by('vin')

    pages = Paginator(vin_queryset, 50)

    for each in pages:
        page = pages.page(each.number)
        query_requests = {}
        index = 0
        for vin in page.object_list:
            index += 1
            query_requests.update({
                'query_request_' + str(index): {
                    'vin': vin
                }
            })

        decoder_query_object = {
            'decoder_settings': {
                'display': 'full',
                'version': '7.2.0',
                'common_data': 'on',
                'common_data_packs': {
                    'basic_data': 'on',
                    'engines': 'on'
                }
            },
            'query_requests': query_requests
        }

        post_data = {
            'access_key_id': settings.DECODER_ACCESS_KEY,
            'secret_access_key': settings.DECODER_SECRET_KEY,
            'decoder_query': json.dumps(decoder_query_object)
        }
        try:
            response = requests.post(url, data=post_data)
            if not response.status_code == 200:
                LOGGER.error("Error: Decoding Failed! %s", response)
                return

            json_response = response.json()

            results = json_response.get('query_responses')

            if results:
                for request in results:
                    item = results.get(request)
                    query_request = query_requests.get(request)
                    vin = query_request.get('vin') if query_request else None

                    parse_vin(vin, item)

        except requests.exceptions.RequestException as error:
            LOGGER.error("Error: %s", error)
            return

    return
