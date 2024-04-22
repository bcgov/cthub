from unittest.mock import MagicMock
from django.test import TestCase
from api.keycloak_authentication import KeycloakAuthentication
from rest_framework.test import APIRequestFactory
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework import exceptions

from api.models.permission import Permission
from api.models.user import User
from api.models.user_permission import UserPermission
from api.viewsets.user import UserViewSet
from api.viewsets.upload import UploadViewset
from api.decorators.permission import check_upload_permission
class TestUsers(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.userauth = KeycloakAuthentication()
        self.view = UserViewSet.as_view({'get': 'list'})
        #user with no permission
        self.test_user = User.objects.create(idir='test_user')
        
        #user with admin permission
        self.test_admin_permission = Permission.objects.create(description='admin')
        self.test_admin_user = User.objects.create(idir='test_admin_user')
        self.admin_user_permission = UserPermission.objects.create(user=self.test_admin_user, permission=self.test_admin_permission)
        
        #user with upload permission
        self.test_upload_permission = Permission.objects.create(description='uploader')
        self.test_upload_user = User.objects.create(idir='test_upload_user')
        self.upload_user_permission = UserPermission.objects.create(user=self.test_upload_user, permission=self.test_upload_permission)    
       

    def test_get_user_list(self):
        self.assertTrue(User.objects.filter(idir='test_user').exists())
        request = self.factory.get('/api/users/list')
        request.META = {
            'HTTP_AUTHORIZATION': {
                'idir': 'test_user'
            }
        }
        response = self.view(request)
        self.assertEqual(response.status_code, 403)  # Forbidden status code

        self.assertTrue(User.objects.filter(idir='test_upload_user').exists())
        request_uploader = self.factory.get('/api/users/list')     
        request_uploader.META = {
            'HTTP_AUTHORIZATION': {
                'idir': 'test_upload_user'
            }
        }
        response = self.view(request_uploader)
        self.assertEqual(response.status_code, 403)  # Forbidden status code

        self.assertTrue(User.objects.filter(idir='test_admin_user').exists())
        request_admin = self.factory.get('/api/users/list')
        request_admin.META = {
            'HTTP_AUTHORIZATION': {
                'idir': 'test_admin_user'
            }
        }
        response = self.view(request_admin)
        self.assertEqual(response.status_code, 200)  # OK status code
    def test_not_authenticated_user(self):
        request = self.factory.get('/api/users/list')
        request.META = {
            'HTTP_AUTHORIZATION': {
                'idir': 'test'
            }
        }
        with self.assertRaises(User.DoesNotExist):
            _user, _auth = self.userauth.authenticate(request)

    def test_upload_user_permissions(self):
        # test decorator for user with upload permission
        @check_upload_permission()
        def mock_import_function(request):
            return HttpResponse()
        request = self.factory.post('/api/users/list')
        request.user = 'test_upload_user'
        response = mock_import_function(request)
        self.assertEqual(response.status_code, 200)  # OK status code

        request_admin = self.factory.post('/api/users/list')
        request_admin.user = 'test_admin_user'
        response = mock_import_function(request_admin)
        self.assertEqual(response.status_code, 403)  # Forbidden!

