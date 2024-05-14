from django.apps import AppConfig
import sys


class Config(AppConfig):
    name = "workers"

    def ready(self):
        from workers.scheduled_jobs import (
            schedule_create_minio_bucket,
            schedule_read_uploaded_vins_file,
            schedule_batch_decode_vins,
        )

        if "qcluster" in sys.argv:
            schedule_create_minio_bucket()
            schedule_read_uploaded_vins_file()
            schedule_batch_decode_vins()
