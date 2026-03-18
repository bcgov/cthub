from enum import Enum
from functools import partial
from api.models.decoded_vin_record import VpicDecodedVinRecord, VinpowerDecodedVinRecord
from workers.external_apis.vpic import batch_decode as vpic_batch_decode
from workers.external_apis.vinpower import batch_decode as vinpower_batch_decode


class VPIC(Enum):
    NAME = "vpic"
    DECODE_SUCCESSFUL = "vpic_decode_successful"
    NUMBER_OF_DECODE_ATTEMPTS = "vpic_number_of_decode_attempts"
    MODEL = VpicDecodedVinRecord
    BATCH_DECODER = partial(vpic_batch_decode)


class VINPOWER(Enum):
    NAME = "vinpower"
    DECODE_SUCCESSFUL = "vinpower_decode_successful"
    NUMBER_OF_DECODE_ATTEMPTS = "vinpower_number_of_decode_attempts"
    MODEL = VinpowerDecodedVinRecord
    BATCH_DECODER = partial(vinpower_batch_decode)


SERVICES = [VPIC, VINPOWER]


def get_service(service_name):
    for service in SERVICES:
        if service.NAME.value == service_name:
            return service
    return None


class ICBC_FILE(Enum):
    DELIMITER = "|"
    NA_VALUES = ["NIL", "Unknown", "unknown", "UNKNOWN"]
    DATA_TYPES = {
        "model": str,
        "vin_error_code": str,
        "rate_class_group": str,
        "hybrid_vehicle_flag": str,
        "postal_code": str,
        "make": str,
        "change": str,
        "vin": str,
        "fuel_type": str,
        "use_category": str,
        "policy_type": str,
        "fleet_flag": str,
        "city": str,
        "owner_giver_relationship": str,
        "personal_or_commercial": str,
        "electric_vehicle_flag": str,
        "body_style": str,
        "vin_error_code_description": str,
        "vehicle_type": str,
    }
    COLUMNS_TO_DROP = [
        "ytd_policy_years_earned",
    ]
    NUMERIC_COLUMNS = [
        "rate_class",
        "model_year",
        "net_weight",
        "motorcycle_displacement_size",
        "fleet_number_of_vehicles",
        "vehicle_registration_number",
        "odometer_reading",
        "licenced_gross_vehicle_weight",
        "fleet_identifier",
    ]
    DATE_COLUMNS = [
        "snapshot_date",
        "change_date",
        "vehicle_purchase_date",
        "vehicle_registration_date",
    ]
    MODIFICATION_MAP = {
        "upper": [
            "vin",
            "make",
            "model",
            "postal_code",
            "electric_vehicle_flag",
            "fleet_flag",
            "hybrid_vehicle_flag",
        ],
        "lower": [
            "body_style",
            "fuel_type",
            "owner_giver_relationship",
            "personal_or_commercial",
            "policy_type",
            "rate_class_group",
            "vehicle_type",
            "vin_error_code",
            "vin_error_code_description",
        ],
        "title": ["city", "use_category"],
    }
