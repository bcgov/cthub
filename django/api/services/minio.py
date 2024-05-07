from datetime import timedelta
from minio import Minio

from django.conf import settings

def get_minio_client():
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_USE_SSL,
    )


def get_refined_object_name(object_name):
    prefix = settings.MINIO_PREFIX
    if prefix:
        return prefix + "/" + object_name
    return object_name


def minio_get_object(object_name):
    return get_minio_client().presigned_get_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=get_refined_object_name(object_name),
        expires=timedelta(seconds=3600),
    )


def get_minio_object(object_name):
    try:
        client = get_minio_client()
        refined_object_name = get_refined_object_name(object_name)
        return client.get_object(settings.MINIO_BUCKET_NAME, refined_object_name)
    except:
        raise


def minio_put_object(object_name):
    return get_minio_client().presigned_put_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=get_refined_object_name(object_name),
        expires=timedelta(seconds=7200),
    )


def minio_remove_object(object_name):
    return get_minio_client().remove_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=get_refined_object_name(object_name),
    )
