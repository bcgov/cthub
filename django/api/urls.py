"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.viewsets.icbc_data import IcbcViewset
from api.viewsets.minio import MinioViewSet
from api.viewsets.upload import UploadViewset
from api.viewsets.user import UserViewSet
from api.viewsets.healthcheck import HealthCheckViewset
from api.viewsets.decoded_vin_record import DecodedVinRecordViewset


ROUTER = routers.SimpleRouter(trailing_slash=False)

ROUTER.register(r"icbc-data", IcbcViewset, basename="icbc-data")

ROUTER.register(r"uploads", UploadViewset, basename="uploads")

ROUTER.register(r"minio", MinioViewSet, basename="minio")
ROUTER.register(r"users", UserViewSet)
ROUTER.register(r"healthcheck", HealthCheckViewset, basename="healthcheck")
ROUTER.register(r"decoded-vin-records", DecodedVinRecordViewset)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(ROUTER.urls)),
]
