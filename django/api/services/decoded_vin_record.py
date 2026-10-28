from api.models.decoded_vin_record import VpicDecodedVinRecord, VinpowerDecodedVinRecord


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
            or "hev" in elec
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
