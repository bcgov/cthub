from rest_framework.serializers import ModelSerializer
from api.models.file_requirements import FileRequirements


class FileRequirementsSerializer(ModelSerializer):

    class Meta:
        model = FileRequirements
        fields = ("sheet", "columns", "formats")
