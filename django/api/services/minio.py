from datetime import timedelta
from minio import Minio

from django.conf import settings

MINIO = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_USE_SSL
)

def get_refined_object_name(object_name):
    prefix = settings.MINIO_PREFIX
    if prefix:
        return prefix + '/' + object_name
    return object_name

def minio_get_object(object_name):
    return MINIO.presigned_get_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=get_refined_object_name(object_name),
        expires=timedelta(seconds=3600)
    )


def minio_put_object(object_name):
    return MINIO.presigned_put_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=get_refined_object_name(object_name),
        expires=timedelta(seconds=7200)
    )


def minio_remove_object(object_name):
    return MINIO.remove_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=get_refined_object_name(object_name)
    )
