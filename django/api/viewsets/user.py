from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from api.models.permission import Permission
from api.models.user import User
from api.models.user_permission import UserPermission
from api.serializers.user import UserSerializer
from api.decorators.permission import check_admin_permission

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
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'])
    @method_decorator(check_admin_permission())
    def update_permissions(self, request):
        # make queryset with the users to update?
        permissions = Permission.objects.all()
        error_msg = []
        for user_idir, v in request.data.items():
            print('********** ', v)
            user = User.objects.get(idir=user_idir)
            for permission_description, value in v.items():
                permission_to_update = permissions.get(description=permission_description)
                if value == True:
                    try:
                    # permission should be added
                        UserPermission.objects.get_or_create(user_id=user.id, permission_id=permission_to_update.id)
                    except Exception as error:
                        error_msg.append("{} permission could not be added to {}".format(permission_description, user.idir))
                    
                if value == False:
                # permission should be removed from user_permission
                # make sure they are not removing their own admin permission
                    if request.user == user_idir and permission_description == 'admin':
                        error_msg += 'You can not remove your own admin permission.'
                    else:   
                        try:
                            permission_to_delete = UserPermission.objects.filter(user_id=user.id, permission_id=permission_to_update.id).first()
                            print(permission_to_delete)
                            if permission_to_delete:
                                permission_to_delete.delete()
                        except Exception as error:
                            error_msg.append("{} permission couldn't be removed from {}.".format(permission_description, user.idir))
        ## to do
        ## double check if something exists before trying to delete it
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