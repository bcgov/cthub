import requests
from django.conf import settings


def batch_decode(uploaded_vin_records):
    vpic_vin_key = settings.VPIC_VIN_KEY
    vpic_error_code_name = settings.VPIC_ERROR_CODE_NAME
    vpic_success_error_code = settings.VPIC_SUCCESS_ERROR_CODE
    successful_records = {}
    failed_vins = set()

    url = settings.VPIC_ENDPOINT + "/DecodeVINValuesBatch/"

    request_data = ""
    for record in uploaded_vin_records:
        request_data = request_data + record.vin + ";"

    body = {"format": "json", "data": request_data}
    response = requests.post(url, data=body)
    response.raise_for_status()
    data = response.json()["Results"]
    decoded_vins_map = {}
    for record in data:
        vin = record.get(vpic_vin_key)
        decoded_vins_map[vin] = record

    for record in uploaded_vin_records:
        vin = record.vin
        decoded_record = decoded_vins_map.get(vin)
        if (
            decoded_record is not None
            and decoded_record[vpic_error_code_name] == vpic_success_error_code
        ):
            successful_records[vin] = decoded_record
        else:
            failed_vins.add(vin)

    return {"successful_records": successful_records, "failed_vins": failed_vins}
