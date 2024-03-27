"""
Further reading:
https://www.django-rest-framework.org/api-guide/serializers/
"""
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

from api.models.user import User
from api.models.user_permission import UserPermission
from api.services.permissions import get_permissions_representation

class UserSerializer(ModelSerializer):
    """
    Default Serializer for User
    """
    user_permissions = SerializerMethodField()

    def get_user_permissions(self, obj):
        user_permission = UserPermission.objects.select_related("permission").filter(user_id=obj.id)
        permissions = []
        for each in user_permission:
            permissions.append(each.permission)
        return get_permissions_representation(permissions)
    
    def validate_idir(self, value):
        if isinstance(value, str) and value.strip():
            return value.strip().upper()
        raise ValidationError("IDIR error!")
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ('idir', 'user_permissions')

# requires permissions_map object
class UserListSerializer(ModelSerializer):
    user_permissions = SerializerMethodField()

    def get_user_permissions(self, obj):
        permissions_map = self.context.get("permissions_map")
        permissions = permissions_map.get(obj)
        return get_permissions_representation(permissions)

    class Meta:
        model = User
        fields = ('idir', 'user_permissions')
