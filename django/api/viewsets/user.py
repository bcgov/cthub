from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from api.models.user import User
from api.serializers.user import UserSerializer, UserSaveSerializer

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
        'update': UserSaveSerializer,
        'create': UserSaveSerializer,
    }


    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes[self.action]

        return self.serializer_classes['default']


    @action(detail=False)
    def current(self, request):
        """
        Get the current user
        """
        user = User.objects.filter(idir=request.user).first()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def list(self, request):
        request = self.request
        ##check if user is admin before producing list of all users
        users = User.objects.all()
        current_user = users.filter(idir=request.user).first()
        if current_user:
            current_user_serializer = UserSerializer(current_user)
            current_user_permissions = current_user_serializer.data['user_permissions']
            is_admin = False
            if current_user_permissions:
                for i in current_user_permissions:
                    for v in i.values():
                        if v == 'admin':
                            is_admin = True
                if is_admin == True:
                    serializer = UserSerializer(users, many=True)
                    return Response(serializer.data)