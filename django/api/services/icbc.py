from api.models.icbc import IcbcRecord


def get_icbc_ev_records(vins):
    result = {}
    records = IcbcRecord.objects.filter(vin__in=vins).only(
        "vin",
        "electric_vehicle_flag",
        "fuel_type",
        "hybrid_vehicle_flag",
        "make",
        "model",
        "model_year",
        "vehicle_registration_date",
        "snapshot_date",
    )
    for record in records:
        fuel_type = record.fuel_type
        if (
            record.electric_vehicle_flag == "Y"
            or record.hybrid_vehicle_flag == "Y"
            or fuel_type == "ELECTRIC"
            or fuel_type == "HYDROGEN"
            or fuel_type == "GASOLINEELECTRIC"
        ):
            result[record.vin] = {
                "make": record.make,
                "model": record.model,
                "modelYear": record.model_year,
                "registrationDate": (
                    str(record.vehicle_registration_date)
                    if record.vehicle_registration_date
                    else None
                ),
                "snapshotDate": (
                    str(record.snapshot_date) if record.snapshot_date else None
                ),
            }
    return result
