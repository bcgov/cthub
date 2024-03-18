from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from api.models.user import User
from api.serializers.user import UserSerializer, UserListSerializer
from api.decorators.permission import check_admin_permission
from api.services.user import update_permissions
from api.services.permissions import get_permissions_map

class UserViewSet(GenericViewSet, CreateModelMixin):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    and  `update`  actions.
    """
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = User.objects.all()

    serializer_classes = {
        'default': UserSerializer,
    }


    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes[self.action]

        return self.serializer_classes['default']

    @action(detail=False, methods=['delete'])
    @method_decorator(check_admin_permission())
    def delete(self, request):
        current_user = request.data['current_user']
        user_idir = request.data['userToDelete']
        if current_user != user_idir:
            try:
                User.objects.get(idir=user_idir).delete()
                users = User.objects.all().order_by('idir')
                serializer = UserListSerializer(users, many=True, context={"permissions_map": get_permissions_map(users)})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('you cannot delete your own idir', status=status.HTTP_400_BAD_REQUEST )


    @method_decorator(check_admin_permission())
    def create(self, request):
        return super().create(request)

    @action(detail=False, methods=['put'])
    @method_decorator(check_admin_permission())
    def update_permissions(self, request):
        user_permissions = request.data
        try:
            update_permissions(user_permissions)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response('User permissions were updated!', status=status.HTTP_200_OK)
    
    @action(detail=False)
    def current(self, request):
        """
        Get the current user
        """
        user = User.objects.filter(idir=request.user).first()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @method_decorator(check_admin_permission())
    def list(self, request):
        users = User.objects.all().order_by('idir')
        serializer = UserListSerializer(users, many=True, context={"permissions_map": get_permissions_map(users)})
        return Response(serializer.data)