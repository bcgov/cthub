from api.models.uploaded_vins_file import UploadedVinsFile


def create_vins_file(filename, **kwargs):
    UploadedVinsFile.objects.create(filename=filename, **kwargs)
