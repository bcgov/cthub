from api.models.uploaded_vin_record import UploadedVinRecord
from api.models.decoded_vin_record import VpicDecodedVinRecord, VinpowerDecodedVinRecord
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

        decoded_vin_model.objects.bulk_create(
            decoded_records_to_insert, ignore_conflicts=True
        )
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
    # Resolve from VPIC decoded records
    vpic_records = VpicDecodedVinRecord.objects.filter(vin__in=vins).values(
        "vin",
        "data__FuelTypePrimary",
        "data__ElectrificationLevel",
        "data__Make",
        "data__Model",
        "data__ModelYear",
    )
    for record in vpic_records:
        fuel = (record.get("data__FuelTypePrimary") or "").lower()
        elec = (record.get("data__ElectrificationLevel") or "").lower()
        is_ev = (
            "electric" in fuel
            or "hydrogen" in fuel
            or "fuel cell" in fuel
            or "bev" in elec
            or "phev" in elec
        )
        if is_ev:
            result[record.get("vin")] = {
                "make": record.get("data__Make"),
                "model": record.get("data__Model"),
                "model_year": record.get("data__ModelYear"),
            }

    # Fall back to historical Vinpower records for any VINs not yet in VPIC
    unresolved_vins = [vin for vin in vins if vin not in result]
    if unresolved_vins:
        legacy_records = VinpowerDecodedVinRecord.objects.filter(
            vin__in=unresolved_vins
        ).values(
            "vin", "data__fuel_type", "data__make", "data__model", "data__model_year"
        )
        for record in legacy_records:
            fuel_type = record.get("data__fuel_type")
            if fuel_type and fuel_type in [
                "Electric",
                "Fuel Cell",
                "Electric/Gasoline",
                "Hydrogen",
                "Diesel/Electric",
            ]:
                result[record.get("vin")] = {
                    "make": record.get("data__make"),
                    "model": record.get("data__model"),
                    "model_year": record.get("data__model_year"),
                }
    return result
