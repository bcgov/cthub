from api.models.uploaded_vins_file import UploadedVinsFile


def create_vins_file(filename, icbc=True, **kwargs):
    there_exists_an_in_process_file = UploadedVinsFile.objects.exclude(
        status=UploadedVinsFile.FileStatus.SUCCESS
    ).exists()
    if there_exists_an_in_process_file:
        raise Exception("There exists an in-process file!")

    UploadedVinsFile.objects.create(filename=filename, icbc=icbc, **kwargs)


def get_file_to_process():
    statuses = UploadedVinsFile.FileStatus
    return UploadedVinsFile.objects.exclude(
        status__in=[
            statuses.ERROR,
            statuses.ERROR_SAVING_DUPLICATES,
            statuses.ERROR_TRACKING_CREATED_AND_MODIFIED_RECORDS,
            statuses.ERROR_TRACKING_REMOVED_RECORDS,
            statuses.ERROR_CLEARING_VIN_LOOKUP_TABLE,
            statuses.SUCCESS,
        ]
    ).first()


def get_prev_icbc_file():
    return (
        UploadedVinsFile.objects.filter(
            icbc=True,
            status=UploadedVinsFile.FileStatus.SUCCESS,
        )
        .order_by("-create_timestamp")
        .first()
    )
