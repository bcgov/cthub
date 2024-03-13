"""
Further reading:
https://www.django-rest-framework.org/api-guide/serializers/
"""
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.models.user import User
from api.models.user_permission import UserPermission
from api.serializers.permission import PermissionSerializer

class UserSerializer(ModelSerializer):
    """
    Default Serializer for User
    """
    user_permissions = SerializerMethodField()

    def get_user_permissions(self, obj):
        user_permission = UserPermission.objects.filter(user_id=obj.id)
        permissions = PermissionSerializer(user_permission, read_only=True, many=True)
        admin = False
        uploader = False
        for i in permissions.data:
            if i['description'] == 'admin':
                admin = True
            if i['description'] == 'uploader':
                uploader = True

        return {'admin': admin, 'uploader': uploader}

    class Meta:
        model = User
        fields = ('idir', 'user_permissions')


class UserSaveSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        request = self.context.get('request')
        permissions = validated_data.pop('permissions')
        print(request)
        print(permissions)
        #check if user exists, if not add them

        #update user_permissions
    
