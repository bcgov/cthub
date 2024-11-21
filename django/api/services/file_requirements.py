from api.models.file_requirements import FileRequirements


def get_file_requirements(dataset_name):
    return FileRequirements.objects.filter(dataset__name=dataset_name).first()
