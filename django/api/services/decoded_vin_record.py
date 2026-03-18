from api.models.uploaded_vin_record import UploadedVinRecord
from api.constants.decoder import get_service
from api.services.uploaded_vin_record import (
    set_decode_successful,
    get_number_of_decode_attempts,
    set_number_of_decode_attempts,
)


def save_decoded_data(
    uploaded_vin_records,
    service_name,
    decoded_data,
):
    decoded_records_to_insert = []
    successful_records = decoded_data["successful_records"]
    failed_vins = decoded_data["failed_vins"]

    service = get_service(service_name)
    if service:
        decoded_vin_model = service.MODEL.value
        for uploaded_record in uploaded_vin_records:
            vin = uploaded_record.vin
            if vin in successful_records:
                decoded_datum = successful_records.get(vin)
                set_decode_successful(service_name, uploaded_record, True)
                decoded_records_to_insert.append(
                    decoded_vin_model(vin=vin, data=decoded_datum)
                )
            elif vin in failed_vins:
                set_decode_successful(service_name, uploaded_record, False)

            set_number_of_decode_attempts(
                service_name,
                uploaded_record,
                get_number_of_decode_attempts(service_name, uploaded_record) + 1,
            )

        decoded_vin_model.objects.bulk_create(decoded_records_to_insert, ignore_conflicts=True)
        UploadedVinRecord.objects.bulk_update(
            uploaded_vin_records,
            [
                "update_timestamp",
                service.DECODE_SUCCESSFUL.value,
                service.NUMBER_OF_DECODE_ATTEMPTS.value,
            ],
        )


def get_vinpower_decoded_ev_vins(vins):
    result = {}
    service = get_service("vinpower")
    decoded_records_model = service.MODEL.value
    records = decoded_records_model.objects.filter(vin__in=vins).values(
        "vin", "data__Fuel Type", "data__Make", "data__Model", "data__Model Year"
    )
    for record in records:
        fuel_type = record.get("data__Fuel Type")
        if fuel_type and fuel_type == "Electric":
            result[record.get("vin")] = {
                "make": record.get("data__Make"),
                "model": record.get("data__Model"),
                "model_year": record.get("data__Model Year"),
            }
    return result
