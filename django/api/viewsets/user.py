from django.utils.decorators import method_decorator
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from api.models.user import User
from api.serializers.user import UserSerializer
from api.decorators.permission import check_admin_permission
from api.services.user import update_permissions

class UserViewSet(GenericViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    and  `update`  actions.
    """
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = User.objects.all()

    serializer_classes = {
        'default': UserSerializer,
    }


    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes[self.action]

        return self.serializer_classes['default']


    @action(detail=False, methods=['post'])
    @method_decorator(check_admin_permission())
    def new(self, request):
        user_to_insert = request.data['idir'].upper()
        try:
            User.objects.get_or_create(idir=user_to_insert)
            return Response(user_to_insert, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=False, methods=['put'])
    @method_decorator(check_admin_permission())
    def update_permissions(self, request):
        error_msg = update_permissions(self, request)
        if error_msg:
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('User permissions were updated!', status=status.HTTP_201_CREATED)
    
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
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)