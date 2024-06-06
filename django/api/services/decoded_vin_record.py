from api.models.uploaded_vin_record import UploadedVinRecord
from api.decoder_constants import get_service
from api.services.uploaded_vin_record import (
    set_decode_successful,
    get_number_of_decode_attempts,
    set_number_of_decode_attempts,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def save_decoded_data(
    uploaded_vin_records,
    vins_to_insert,
    decoded_records_to_update_map,
    service_name,
    decoded_data,
):
    decoded_records_to_insert = []
    decoded_records_to_update = []
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
                if vin in vins_to_insert:
                    decoded_records_to_insert.append(
                        decoded_vin_model(vin=vin, data=decoded_datum)
                    )
                elif vin in decoded_records_to_update_map:
                    decoded_record_to_update = decoded_records_to_update_map.get(vin)
                    decoded_record_to_update.update_timestamp = timezone.now()
                    decoded_record_to_update.data = decoded_datum
                    decoded_records_to_update.append(decoded_record_to_update)
            elif vin in failed_vins:
                set_decode_successful(service_name, uploaded_record, False)

            set_number_of_decode_attempts(
                service_name,
                uploaded_record,
                get_number_of_decode_attempts(service_name, uploaded_record) + 1,
            )

        decoded_vin_model.objects.bulk_update(
            decoded_records_to_update, ["update_timestamp", "data"]
        )
        decoded_vin_model.objects.bulk_create(decoded_records_to_insert)
        UploadedVinRecord.objects.bulk_update(
            uploaded_vin_records,
            [
                "update_timestamp",
                service.CURRENT_DECODE_SUCCESSFUL.value,
                service.NUMBER_OF_CURRENT_DECODE_ATTEMPTS.value,
            ],
        )


def get_decoded_vins(service_name, vins):
    result = {}
    service = get_service(service_name)
    if service:
        decoded_records_model = service.MODEL.value
        records = decoded_records_model.objects.filter(vin__in=vins)
        for record in records:
            result[record.vin] = record.data
    return result
