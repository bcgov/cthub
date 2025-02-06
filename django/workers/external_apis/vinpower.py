import requests
from django.conf import settings
import json
import xmltodict


def batch_decode(uploaded_vin_records):
    successful_records = {}
    failed_vins = set()
    url = settings.VINPOWER_ENDPOINT + "/decode"

    vins = []
    for record in uploaded_vin_records:
        vins.append(record.vin)
    headers = {"content-type": "application/json"}
    response = requests.get(url, data=json.dumps(vins), headers=headers)
    response.raise_for_status()

    data = response.json()
    for vin in vins:
        decoded_xml = data.get(vin)
        if decoded_xml is not None:
            dict = xmltodict.parse(decoded_xml)
            atts = dict["VINPOWER"]["VIN"]["DECODED"]["ITEM"]
            decoded_data = {}
            for att in atts:
                decoded_data[att["@name"]] = att["@value"]
            successful_records[vin] = decoded_data
        else:
            failed_vins.add(vin)

    return {"successful_records": successful_records, "failed_vins": failed_vins}
