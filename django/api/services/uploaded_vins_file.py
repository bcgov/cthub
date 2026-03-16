from api.models.uploaded_vins_file import UploadedVinsFile


def create_vins_file(filename, icbc=True, **kwargs):
    UploadedVinsFile.objects.create(filename=filename, icbc=icbc, **kwargs)
