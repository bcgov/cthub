from api.models.uploaded_vins_file import UploadedVinsFile
from api.services.minio import get_minio_object
from api.constants.decoder import ICBC_FILE


def create_vins_file(filename, icbc=True, **kwargs):
    there_exists_an_in_process_file = UploadedVinsFile.objects.exclude(
        status=UploadedVinsFile.FileStatus.SUCCESS
    ).exists()
    if there_exists_an_in_process_file:
        raise Exception("There exists an in-process file!")

    file_response = get_minio_object(filename)
    line = file_response.readline()
    line_byte_length = len(line)
    decoded_line = line.decode("utf-8")
    headers = [
        item.strip().lower() for item in decoded_line.split(ICBC_FILE.DELIMITER.value)
    ]
    UploadedVinsFile.objects.create(
        filename=filename,
        icbc=icbc,
        headers=headers,
        headers_byte_length=line_byte_length,
        byte_offset=line_byte_length,
        **kwargs
    )


def get_file_to_process():
    statuses = UploadedVinsFile.FileStatus
    return UploadedVinsFile.objects.exclude(
        status__in=[
            statuses.ERROR,
            statuses.ERROR_SAVING_FIRST_SNAPSHOT_DATE,
            statuses.ERROR_SAVING_DUPLICATES_AND_LOOKUPS,
            statuses.ERROR_TRACKING_REMOVED_RECORDS,
            statuses.ERROR_TRACKING_CREATED_AND_MODIFIED_RECORDS,
            statuses.SUCCESS,
        ]
    ).first()
