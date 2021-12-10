import logging
import requests

from django.core.paginator import Paginator

from api.models.icbc_registration_data import IcbcRegistrationData
from api.models.vin_decoded_information import VINDecodedInformation

LOGGER = logging.getLogger(__name__)


def decoder():
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/'
    json_response = None
    model_year = None

    vin_queryset = IcbcRegistrationData.objects.values_list(
        'vin', flat=True
    ).order_by('vin')

    pages = Paginator(vin_queryset, 50)

    for each in pages:
        page = pages.page(each.number)
        vin_batch = ';'.join(page.object_list)
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
                    if item.get('ModelYear'):
                        model_year = int(item.get('ModelYear'))
                    VINDecodedInformation.objects.create(
                        fuel_type_primary=item.get('FuelTypePrimary'),
                        make=item.get('Make'),
                        manufacturer=item.get('Manufacturer'),
                        model_year=model_year,
                        model=item.get('Model'),
                        vin=item.get('VIN')
                    )
        except requests.exceptions.RequestException as error:
            LOGGER.error("Error: %s", error)
            return

    return
