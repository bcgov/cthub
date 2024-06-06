from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.models.permission import Permission
from api.models.user_permission import UserPermission


class PermissionSerializer(ModelSerializer):
    description = SerializerMethodField()

    def get_description(self, obj):
        permission = Permission.objects.filter(id=obj.permission_id).first()
        if permission:
            return permission.description

    class Meta:
        model = Permission
        fields = (
            "id",
            "description",
        )
