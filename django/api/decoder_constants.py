import os
from enum import Enum
from functools import partial
from api.models.decoded_vin_record import VpicDecodedVinRecord, VinpowerDecodedVinRecord
from workers.external_apis.vpic import batch_decode as vpic_batch_decode
from workers.external_apis.vinpower import batch_decode as vinpower_batch_decode


class VPIC(Enum):
    NAME = "vpic"
    CURRENT_DECODE_SUCCESSFUL = "vpic_current_decode_successful"
    NUMBER_OF_CURRENT_DECODE_ATTEMPTS = "vpic_number_of_current_decode_attempts"
    MODEL = VpicDecodedVinRecord
    BATCH_DECODER = partial(vpic_batch_decode)


class VINPOWER(Enum):
    NAME = "vinpower"
    CURRENT_DECODE_SUCCESSFUL = "vinpower_current_decode_successful"
    NUMBER_OF_CURRENT_DECODE_ATTEMPTS = "vinpower_number_of_current_decode_attempts"
    MODEL = VinpowerDecodedVinRecord
    BATCH_DECODER = partial(vinpower_batch_decode)


SERVICES = [VPIC, VINPOWER]


def get_service(service_name):
    for service in SERVICES:
        if service.NAME.value == service_name:
            return service
    return None
