from django.conf import settings
from api.services.minio import get_minio_client, get_minio_object
from api.models.uploaded_vins_file import UploadedVinsFile
from api.services.uploaded_vins_file import get_file_to_process
from api.services.uploaded_vin_record import parse_and_save
from api.services.icbc import icbc_parse_and_save
from api.constants.decoder import FILE_PROCESSING_DIRECTORY
from django.db import transaction
from pathlib import Path


def create_minio_bucket():
    bucket_name = settings.MINIO_BUCKET_NAME
    client = get_minio_client()
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)


def read_uploaded_vins_file():
    vins_file = get_file_to_process()
    if vins_file is None:
        return
    status = vins_file.status
    filename = vins_file.filename
    byte_offset = vins_file.byte_offset
    if status == UploadedVinsFile.FileStatus.NEW:
        file_processing_dir = Path(FILE_PROCESSING_DIRECTORY)
        for item in file_processing_dir.iterdir():
            item.unlink()
        f = get_minio_object
        args = (filename,)
    else:
        f = open
        args = (f"{FILE_PROCESSING_DIRECTORY}/{filename}", "rb")
    with (
        f(*args) as file_response,
        transaction.atomic(),
    ):
        if status != UploadedVinsFile.FileStatus.NEW:
            file_response.seek(byte_offset)
        if vins_file.icbc:
            icbc_parse_and_save(vins_file, file_response)
        else:
            parse_and_save(vins_file, file_response)


def remove_cleaned_datasets():
    try:
        client = get_minio_client()
        objects = client.list_objects(
            settings.MINIO_BUCKET_NAME, prefix="cleaned_datasets/"
        )
        for obj in objects:
            client.remove_object(settings.MINIO_BUCKET_NAME, obj.object_name)
    except Exception:
        print("Error occurred when removing cleaned-datasets.")
